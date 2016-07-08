import argh
import pandas as pd
from pydub.audio_segment import AudioSegment
import yaml
from argh import arg
from splice import parse_splits, expand_data, aud_from_log, update_splits, align_blueprints, insert_gaps

@arg('bp', type=str, help="name of blueprint for audio")
@arg('stories', type=yaml.load, help="names of audio files corresponding to blueprint")
def make_audio(bp, stories, audout="default.wav", bpout="default.csv"):
    """Generate wav with concatenated segments from blueprint."""
    print "----Loading Data----"
    df = pd.read_csv(bp)
    print df

    print "----Loading Audio----"
    story_dict = {}
    for key, fname in stories.iteritems():
        story_dict[key] = AudioSegment.from_file(fname)

    print "----Exporting Audio----"
    audio = aud_from_log(df, **story_dict)
    audio.export(audout, format=audout.split('.')[-1])

    print "----Saving Blueprint For Export----"
    df['old_name'] = df['name']
    df['name'] = audout
    update_splits(df)
    df.to_csv(bpout)

def align(src, ref, outname='aligned.csv'):
    """Align src blueprint to ref blueprint.
    """
    print "----Aligning to %s----"%ref
    src = pd.read_csv(src, index_col = None) if type(src) == str else src
    ref = pd.read_csv(ref, index_col = None) if type(ref) == str else ref
    if 'old_name' not in src:
        left_on = ['name', 'order']
    else:
        left_on = ['old_name', 'order']
    bp = align_blueprints(src, ref, left_on)
    print bp
    bp.to_csv(outname)
    
@arg('stories', nargs='*')
def unscramble(bp, stories, suffix):
    if type(bp) == str: bp = pd.read_csv(bp)
    intact = bp.sort(['old_name', 'order'])
    stories = {story : AudioSegment.from_file(story) for story in stories}
    for ii, g in intact.groupby(['old_name']):
        aud = aud_from_log(g, **stories)
        try: ftype = suffix.split('.')[-1]
        except IndexError: ftype = "wav"
        aud.export(ii + suffix, ftype)

parser = argh.ArghParser()
parser.add_commands([parse_splits, insert_gaps, expand_data, align, make_audio, unscramble])

# Command Line ---------------------------------------------------------------
def main(): parser.dispatch()

if __name__ == '__main__':
    main()
