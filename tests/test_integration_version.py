
def test_version_command_distech_4_13(capsys, main_parser_fixture, set_enviro_distech_4_13):
        args = main_parser_fixture.parse_args('version'.split())
        args.func(args)

        captured = capsys.readouterr()
        assert captured.out == "Version: 4.13\n"


def test_version_command_vykon_4_14(capsys, main_parser_fixture, set_enviro_vykon_4_14):
        args = main_parser_fixture.parse_args('version'.split())
        args.func(args)

        captured = capsys.readouterr()
        assert captured.out == "Version: 4.14\n"