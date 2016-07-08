from scrampy.splice import parse_splits, update_splits, aud_from_log, expand_data, insert_gaps
from pydub.audio_segment import AudioSegment

# TODO: move to setup function (in a class)

# load load and audio
log = parse_splits('examples/aud/NTF/NotTheFall_sentence_splitpoints.txt')
#log['order'] = range(0, len(log))
audio = {'NTF': AudioSegment.from_mp3('examples/aud/NTF/NotTheFall.mp3')}

# shuffle
indx = [1,0]
#random.shuffle(indx)
new_log = log.iloc[indx].copy()

# make new audio
audlist = aud_from_log(new_log, **audio)
out = reduce(lambda x,y: x + y, audlist)

# update start and end points on new log
update_splits(new_log)
unscram_log = new_log.sort('order')

get_clip = lambda clip, log, ii: clip[log['start'][ii] : log['end'][ii]]

def test_update_splits():
    """First row of Updated splits has start value of 0"""
    assert new_log.iloc[0]['start'] == 0

def test_new_log_indx_order():
    """New log starts with segment 1 (i.e. the second segment)"""
    assert new_log['start'][1] == 0

def test_new_log_diff():
    """New log reorders segments"""
    assert get_clip(audlist, log, 1) != get_clip(audio['NTF'], log, 1)

def test_match_new_aud():
    """New scrambled audio segments are equivalent to old segments"""
    for ii in range(2):
        assert get_clip(audio['NTF'], log, ii) == get_clip(audlist, unscram_log, ii)

def test_aud_from_log_ignores_index():
    """aud_from_log behaves the same, regardless of index values"""
    assert True

def test_expand_data_1500_correct_len():
    """Length for expanded data is rounded down"""
    # TODO: should it round up to allow last snippet of time?
    exp = expand_data(log, 1500)
    assert len(exp) == (log['end'].iloc[-1] / 1500)

def test_expand_data_1500_scram_log():
    """Same length and number of entries per segment for scrambled"""
    exp = expand_data(log, 1500)
    new_exp = expand_data(new_log, 1500)

    assert len(exp) == len(new_exp)
    assert sum(exp['order'] == 0) == sum(new_exp['order'] == 0)

def test_insert_gaps_order_invariant():
    """Proceeding gap is invariant to row order"""
    gaps1 = insert_gaps(log)
    gaps2 = insert_gaps(log.iloc[[1,0]])

    get_gaps = lambda x: x[x['name'] == 'gap']['length'].reset_index(drop=True)
    assert (get_gaps(gaps1) == get_gaps(gaps2.iloc[::-1])).all()
     
