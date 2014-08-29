scrampy
=======
Scrambling audio like it aint nobody's business.

Examples
--------
scrampy uses something called blueprints.
See "How it Works" for all the juicy details on how these work.
All examples are run from the shell (and untested on Windows :O).

### Scrambline and Unscrambling

Below, we use the blueprint found in `examples/simple/interl_blueprint.csv`:
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>name</th>      <th>start</th>      <th>end</th>      <th>length</th>      <th>order</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>    NTF</td>      <td>     0</td>      <td>  8921</td>      <td>  8921</td>      <td> 0</td>    </tr>    <tr>      <th>1</th>      <td> pieman</td>      <td> 14000</td>      <td> 26970</td>      <td> 12970</td>      <td> 0</td>    </tr>    <tr>      <th>2</th>      <td>    NTF</td>      <td>  8921</td>      <td> 19694</td>      <td> 10773</td>      <td> 1</td>    </tr>    <tr>      <th>3</th>      <td> pieman</td>      <td> 26970</td>      <td> 41620</td>      <td> 14650</td>      <td> 1</td>    </tr>  </tbody></table>

This blueprint interleaves two audio narratives, to generate the interleaved audio.
The narratives are in `aud/{narrative_folder}`.

    cd examples
    scrampy make-audio simple/interl_blueprint.csv \
        "{pieman: aud/pieman/pieman.mp3, NTF: aud/NTF/NotTheFall.mp3}"

This produces interleaved audio as `default.wav` in the current directory.
Notice that there is a new blueprint titled `default.csv` produced as well.
This blueprint contains start and stop times with respect to the audio file just produced..
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>name</th>      <th>start</th>      <th>end</th>      <th>length</th>      <th>order</th>      <th>old_name</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td> default.wav</td>      <td>     0</td>      <td>  8921</td>      <td>  8921</td>      <td> 0</td>      <td>    NTF</td>    </tr>    <tr>      <th>1</th>      <td> default.wav</td>      <td>  8921</td>      <td> 21891</td>      <td> 12970</td>      <td> 0</td>      <td> pieman</td>    </tr>    <tr>      <th>2</th>      <td> default.wav</td>      <td> 21891</td>      <td> 32664</td>      <td> 10773</td>      <td> 1</td>      <td>    NTF</td>    </tr>    <tr>      <th>3</th>      <td> default.wav</td>      <td> 32664</td>      <td> 47314</td>      <td> 14650</td>      <td> 1</td>      <td> pieman</td>    </tr>  </tbody></table>

scrampy can use this to pull out segments corresponding to just one story. 
For example, to align it with `aud/pieman/pieman_blueprint.csv`, which describes just one of the audio sources:
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>name</th>      <th>order</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td> pieman</td>      <td> 0</td>    </tr>    <tr>      <th>1</th>      <td> pieman</td>      <td> 1</td>    </tr>  </tbody></table>

to align, we would just do..

    scrampy align default.csv aud/pieman/pieman_blueprint.csv

Note that all you need is name and order columns in the second file.
By default, the output is saved as aligned.csv, so we can use this file to reverse the process:

    scrampy make-audio aligned.csv "{default.wav: default.wav}" \
        --audout pieman.wav --bpout pieman_blueprint.csv

### Inserting gaps between each segment
Gaps can be inserted after each row using the `insert-gaps` command.
For example, if your current directory is `examples`

    scrampy insert-gaps simple/interl_blueprint.csv                 # print new blueprint
    scrampy insert-gaps simple/interl_blueprint.csv -o new_bp.csv  # save as new_bp.csv

Now, we just need to specify where the gaps file is, in addition to other audio files.

    scrampy make-audio new_bp.csv \
        "{pieman: aud/pieman/pieman.mp3, NTF: aud/NTF/NotTheFall.mp3, gap: aud/silence.mp3}" \
        --audout gaps.wav --bpout gaps.csv

Notice that when we generated audio from this blueprint, each segment+gap in `gaps.csv` ends on a 1500ms TR:
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>name</th>      <th>start</th>      <th>end</th>      <th>length</th>      <th>order</th>      <th>old_name</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td> gaps.wav</td>      <td>     0</td>      <td>  8921</td>      <td>  8921</td>      <td> 0</td>      <td>    NTF</td>    </tr>    <tr>      <th>1</th>      <td> gaps.wav</td>      <td>  8921</td>      <td> 10500</td>      <td>  1579</td>      <td>-1</td>      <td>    gap</td>    </tr>    <tr>      <th>2</th>      <td> gaps.wav</td>      <td> 10500</td>      <td> 23470</td>      <td> 12970</td>      <td> 0</td>      <td> pieman</td>    </tr>    <tr>      <th>3</th>      <td> gaps.wav</td>      <td> 23470</td>      <td> 25500</td>      <td>  2030</td>      <td>-1</td>      <td>    gap</td>    </tr>    <tr>      <th>4</th>      <td> gaps.wav</td>      <td> 25500</td>      <td> 36273</td>      <td> 10773</td>      <td> 1</td>      <td>    NTF</td>    </tr>    <tr>      <th>5</th>      <td> gaps.wav</td>      <td> 36273</td>      <td> 37500</td>      <td>  1227</td>      <td>-1</td>      <td>    gap</td>    </tr>    <tr>      <th>6</th>      <td> gaps.wav</td>      <td> 37500</td>      <td> 52150</td>      <td> 14650</td>      <td> 1</td>      <td> pieman</td>    </tr>    <tr>      <th>7</th>      <td> gaps.wav</td>      <td> 52150</td>      <td> 54000</td>      <td>  1850</td>      <td>-1</td>      <td>    gap</td>    </tr>  </tbody></table>

Order for gaps is set to -1 for all by default, since it doesn't really matter.

How it Works
------------
### Blueprints
scrampy uses spreadsheets saved in csv format to construct audio from different sources.
The spreadsheets are refered to as blueprints.
For example, the blueprint in `examples/simple/interl_blueprint.csv` looks like this:

<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>name</th>      <th>start</th>      <th>end</th>      <th>length</th>      <th>order</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>    NTF</td>      <td>     0</td>      <td>  8921</td>      <td>  8921</td>      <td> 0</td>    </tr>    <tr>      <th>1</th>      <td> pieman</td>      <td> 14000</td>      <td> 26970</td>      <td> 12970</td>      <td> 0</td>    </tr>    <tr>      <th>2</th>      <td>    NTF</td>      <td>  8921</td>      <td> 19694</td>      <td> 10773</td>      <td> 1</td>    </tr>    <tr>      <th>3</th>      <td> pieman</td>      <td> 26970</td>      <td> 41620</td>      <td> 14650</td>      <td> 1</td>    </tr>  </tbody></table>

Here is what each column describes:

* name: name describing source of audio
* start, end: interval in milliseconds where segment is located in audio corresponding to {name}
* length: length of that segment in milliseconds
* order: order of segment with respect to source in name column

Basically, each segment should have a unique combination of **name** and **order** (unless it's being repeated).

### Creating blueprints
As long as it has the columns listed above, and uses milliseconds, it's a blueprint!
There is also a helper command, `parse-splits`, that can generate a basic blueprints
from a csv that just gives the name and break points--e.g.:

<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>name</th>      <th>break</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td> NTF</td>      <td> 0:00.000</td>    </tr>    <tr>      <th>1</th>      <td> NTF</td>      <td> 0:08.921</td>    </tr>    <tr>      <th>2</th>      <td> NTF</td>      <td> 0:19.694</td>    </tr>  </tbody></table>

Notice that here, **you can give breaks in either milliseconds or clock time**.
    
Help
----

`scrampy -h` shows possible commands

`scrampy {CMD_NAME}` shows help for a command (e.g. `scrampy align -h`)
