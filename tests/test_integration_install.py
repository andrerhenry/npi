import pytest

def test_install_command(main_parser_fixture, set_enviro_distech_4_13):
        user_input = 'install vykonPro'
        args = main_parser_fixture.parse_args(user_input.split())
        args.func(args)
        
        module_path = (set_enviro_distech_4_13/'modules')
        package_list = ['vykonPro-doc.jar', 'vykonPro-rt.jar', 'vykonPro-ux.jar', 'vykonPro-wb.jar']
        for module in package_list:
                assert (module_path/module).exists()
        for module in package_list:
                (module_path/module).unlink()

        
        