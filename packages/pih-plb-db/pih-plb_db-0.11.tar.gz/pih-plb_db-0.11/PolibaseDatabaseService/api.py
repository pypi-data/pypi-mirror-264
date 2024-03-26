import ipih

import os
from pih import A
from pih.tools import j, js, n

TEST_NAME: str = "test"
TEST_SOURCE_NAME: str = "stub"
TEST: bool = False


class PolibaseDBApi:
    @staticmethod
    def create_dump(file_name: str | None = None, test: bool | None = None) -> None:
        test = TEST if n(test) else test
        local_mount_point: str = "C:"
        nas_mount_point: str = "K:"
        polibase_test_mount_point: str = "L:"
        polibase_name: str = "Polibase"
        database_dump_name: str = "DatabaseDump"
        local_polibase_database_dump_folder_name: str = j(
            (polibase_name, database_dump_name)
        )
        nas_polibase_database_dump_folder_name: str = j(
            (polibase_name, database_dump_name), "/"
        )
        polibase_folder_path: str = (
            local_mount_point + f"/{local_polibase_database_dump_folder_name}/"
        )

        dump_file_extension: str = "DMP"
        archived_dump_file_extension: str = "zip"
        file_name_result: str = "IN"

        if test:
            file_name = TEST_NAME
        else:
            if n(file_name):
                file_name = A.D.now_to_string(A.CT_P.DB_DATETIME_FORMAT)

        file_name_result = A.PTH.add_extension(file_name_result, dump_file_extension)
        file_database_dump_name_out: str = A.PTH.add_extension(
            file_name, dump_file_extension
        )
        print("test", test)
        if test:
            polibase_folder_path_src: str = polibase_folder_path
            polibase_folder_path = A.PTH.join(polibase_folder_path, TEST_NAME)
            os.system(
                f"robocopy {A.PTH.join(polibase_folder_path_src, TEST_SOURCE_NAME)} {polibase_folder_path} {file_database_dump_name_out}"
            )
        polibase_test_folder_path: str = (
            f"//{A.CT_H.POLIBASE_TEST.NAME}/{local_polibase_database_dump_folder_name}"
        )
        archive_type: str = A.CT_F_E.ARCHIVE
        nas_folder_path: str = (
            f"//{A.CT_H.NAS.NAME}/backups/{nas_polibase_database_dump_folder_name}"
        )

        nas_user: str = "nak"
        nas_password: str = "Soad7623!"
        archiver_program_path: str = 'C:/"Program Files"/7-Zip/7z'

        file_out_name = A.PTH.add_extension(file_name, archived_dump_file_extension)
        par_file_name = "backpar.txt"
        nas_create_connection_command = js(
            (
                "net",
                "use",
                nas_mount_point,
                A.PTH.adapt_for_windows(nas_folder_path),
                j(("/user:", nas_user)),
                nas_password,
            )
        )
        polibase2_create_connection_command = js(
            (
                "net",
                "use",
                polibase_test_mount_point,
                A.PTH.adapt_for_windows(polibase_test_folder_path),
            )
        )
        nas_copy_command = (
            f"robocopy {polibase_folder_path} {nas_mount_point}/ {file_out_name} /J"
        )
        polibase_test_copy_command = f"robocopy {polibase_folder_path} {polibase_test_mount_point}/ {file_database_dump_name_out} /J"
        os.chdir(polibase_folder_path)
        # step 1
        if not test:
            A.E.backup_notify_about_polibase_creation_db_dumb_start()
        if not test:
            os.system(
                f"exp userid=POLIBASE/POLIBASE owner=POLIBASE file={file_database_dump_name_out} parfile={par_file_name}"
            )
        if not test:
            A.E.backup_notify_about_polibase_creation_db_dumb_complete(
                os.path.getsize(
                    A.PTH.join(polibase_folder_path, file_database_dump_name_out)
                )
            )

        # step 2: connect net location with credentials
        os.system(nas_create_connection_command)
        os.system(polibase2_create_connection_command)

        # step 3
        if not test:
            A.E.backup_notify_about_polibase_creation_archived_db_dumb_start()
        os.system(
            f"{archiver_program_path} a -t{archive_type} {file_out_name} {file_database_dump_name_out}"
        )
        if not test:
            A.E.backup_notify_about_polibase_creation_archived_db_dumb_complete(
                os.path.getsize(A.PTH.join(polibase_folder_path, file_out_name))
            )

        # step 4
        if not test:
            A.E.backup_notify_about_polibase_coping_archived_db_dumb_start(
                A.CT_H.NAS.ALIAS.upper()
            )
        os.system(nas_copy_command)
        if not test:
            A.E.backup_notify_about_polibase_coping_archived_db_dumb_complete(
                A.CT_H.NAS.ALIAS.upper()
            )

        # step 5
        if not test:
            A.E.backup_notify_about_polibase_coping_db_dumb_start(
                A.CT_H.POLIBASE_TEST.ALIAS.upper()
            )
        os.system(polibase_test_copy_command)
        if not test:
            A.E.backup_notify_about_polibase_coping_db_dumb_complete(
                A.CT_H.POLIBASE_TEST.ALIAS.upper()
            )

        # step 6
        polibase_test_previous_file_delete_command: str = js(
            ("del", A.PTH.join(polibase_test_mount_point, file_name_result))
        )
        polibase_file_rename_command: str = js(
            (
                "ren",
                A.PTH.join(polibase_test_mount_point, file_database_dump_name_out),
                file_name_result,
            )
        )

        os.system(polibase_test_previous_file_delete_command)
        os.system(polibase_file_rename_command)

        # step 7: disconnect net location with credentials
        os.system(js(("net use", nas_mount_point, "/delete /y")))
        os.system(js(("net use", polibase_test_mount_point, "/delete /y")))

        # step 8
        os.system(js(("del", file_database_dump_name_out)))
        os.system(js(("del", file_out_name)))
