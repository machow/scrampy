from scrampy.splice import parse_old_logs, parse_splits, expand_data

def test_parse_old_logs():
    log_file = 'tests/data/log/Overview_intact_mingap_1000_log'
    old_bp  = parse_old_logs(log_file + '.txt', name='overview')
    crnt_bp = parse_splits(log_file + '.csv')

    assert (old_bp == crnt_bp).all().all()
