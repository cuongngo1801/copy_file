"""This method will be copy the page source file from C disk to share drive"""
import os
import subprocess
import shutil

class CopyFile():
    def __init__(self) -> None:
        self.run_copy = False
        if not os.path.isdir(r'M:'):
            CopyFile.__connnect_with_network()
            print('Connect with share drive')
        CopyFile.check_capacity_disk_local()


    """Get_path_page_source return the dictionary type, it contains a {file}:{path_file}"""
    def get_path_page_source(self,path) -> dict:
        path_file = {f: os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".txt")}
        return path_file

    def get_path_folder(self, path) -> dict:
        path_folder = {f: os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))}
        return path_folder

    def get_path_pkl_file(self,path) -> dict:
        path_file_pkl = {f: os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".pkl")}
        return path_file_pkl
    
    @staticmethod
    def __connnect_with_network() -> None:
        # cmd = r"net use m: \\172.111.0.250\bi_innonet\MR"
        # os.system(cmd)
        subprocess.call(r'net use m: \\172.111.0.250\bi_innonet\MR /user:bi_innonet K@fh33alqpfbq', shell=True)
    
    def check_capacity_disk_local(self):
        obj_Disk  = shutil.disk_usage("/")

        print("Total: %d GiB" % (obj_Disk.total // (2**30)))
        print("Used: %d GiB" % (obj_Disk.used // (2**30)))
        print("Free: %d GiB" % (obj_Disk.free // (2**30)))
        percent = (round(obj_Disk.used/obj_Disk.total*100,3))
        print(f"percent:{percent}")
        if percent >50:
            self.run_copy = True

def compare_value(path_file, path_drive, check_all_file = False) -> dict:
    sub_folder = {}
    for file in path_file.keys():
        if file in path_drive.keys() and not os.path.isfile(path_file[file]) and len(path_drive[file]) > 1:
            print('(compare_value) Check other folders',path_file[file])
            print(os.listdir(path_file[file]))
            sub_folder[file] = path_file[file]
            check_all_file = True

        elif (not file in path_drive.keys() and not os.path.isfile(path_file[file])) or \
        (file in path_drive.keys() and not os.path.isfile(path_file[file]) and len(path_drive[file])==0):
            print(f'(compare_value) Repare copy folder ->> {path_file[file]}')
            dst = process_path_to_copy(path_file[file])
            copy_folder(path_file[file], dst)
        elif (not file in path_drive.keys() and os.path.isfile(path_file[file])) or \
            (len(path_drive[file]) > 1 and file in path_drive.keys()):
            print(f'(compare_value) Repare copy file ->>{path_file[file]} to {path_drive[file]}') 
            copy_files(path_file[file], path_drive[file])
        else:
            check_all_file = True


    return sub_folder, check_all_file

def process_path_to_copy(src, dst='') -> str:
    if len(dst) <1:
        dst = path_m
    list_src = src.split("\\")
    list_dst = dst.split('\\')

    if list_dst[-1] in list_src and any([*map(lambda x: x in list_src,list_dst)]):
        index = list_src.index(list_dst[-1])
        list_dst.extend(list_src[index:])
        dst = '\\'.join(list_dst)
    else:
        del list_src[0:2]
        list_dst.extend(list_src)
        dst = '\\'.join(list_dst)
    return dst

def copy_folder(src, dst) -> None:
    SUCCESS = 0

    if not os.path.isdir(dst):
        os.makedirs(dst, exist_ok=True)
        print('(copy_folder) Create dir:',dst)

    cmd = 'xcopy '+ src +' '+dst + ' /e /i'
    print('(copy_folder) cmd: ',cmd)
    if os.system(cmd) == SUCCESS:
        print('(copy_folder) Copy to successful')
    else:
        print('(copy_folder) Copy file to failed, please check again')


def copy_files(src, dst) -> None:
    SUCCESS = 0
    cmd = 'copy '+ src +' '+dst 
    print('(copy_files) cmd: ',cmd)
    if os.system(cmd) == SUCCESS:
        print('(copy_files) Copy to successful')
    else:
        print('(copy_files) Copy file to failed, please check again')

def delete_folder(folder) -> None:
    SUCCESS = 0
    # cmd = 'rmdir /s '+ folder + ' /Q'
    # print('(delete_folder)',cmd)
    # if os.system(cmd) == SUCCESS:
    #     print('(delete_folder) Delete to successful')
    # else:
    #     print('(delete_folder) Delete to failed, please check again')
    for file_name in os.listdir(folder):
    # construct full file path
        file = folder + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)

def copy_processing(path, check_all_object_after_copy = False) -> bool:
    sub_path_list = {}
    check_pass = 0
    if len(path)>=1:
        for folder in path.keys():
            print('(copy_processing) Go to folder: ',folder)
            sub_folder = os.listdir(path[folder])
            #['AMZ', 'Keepa', 'New Text Document.txt']
            print('(copy_processing) Number of object in local',len(sub_folder))
            if len(sub_folder)>=1:
                for sub in sub_folder:
                    print(f'(copy_processing) Sub folder in {path[folder]}: {sub}')
                    # Check file
                    if os.path.isfile(os.path.join(path[folder],sub)):
                        print('(copy_processing) Prepare to check file in drive')
                        path_file_local = {sub:os.path.join(path[folder],sub)}
                        path_file_drive = {sub:os.path.join(path[folder],sub).replace(path_root,path_m)}
                        print(f'(copy_processing) Path file local:{path_file_local}, path file drive:{path_file_drive}')

                        if not os.path.exists(path_file_drive[sub]):
                            print('(copy_processing) Path file drive is not exist ==> repare goto (compare_value)',path_file_drive[sub])
                            _, check_all_file= compare_value(path_file_local, path_file_drive)
                            if not check_all_file:
                                print('check_pass +=1',path_file_drive[sub])
                                check_pass +=1

                    # Check folder 
                    if os.path.isdir(os.path.join(path[folder],sub)):
                        print('(copy_processing) Prepare to check folder in drive')

                        path_folder_local = {sub:os.path.join(path[folder],sub)}
                        path_folder_drive = {sub:os.path.join(path[folder],sub).replace(path_root,path_m)}
                        print(f'(copy_processing) Path folder local:{path_folder_local}, path folder drive:{path_folder_drive}')

                        if not os.path.exists(path_folder_drive[sub]):
                            print(f'(copy_processing) Path folder is NOT exist==> repare to clean path_folder_drive {path_folder_drive[sub]}')
                            path_folder_drive = {sub:''}
                            print(path_folder_drive, path_folder_local)
                            sub_path_list,check_all_file = compare_value(path_folder_local,path_folder_drive)
                        elif os.path.exists(path_folder_drive[sub]):
                            print(f'(copy_processing) Path folder exist {path_folder_drive[sub]}')
                            sub_path_list, check_all_file = compare_value(path_folder_local,path_folder_drive)
                            if not check_all_file:
                                print('check_pass +=1 :',path_folder_drive[sub])
                                check_pass +=1

                        copy_processing(sub_path_list)
    if check_all_object_after_copy:
        print('check_pass',check_pass)
        if check_pass>0:
            return False
        else:
            return True    




if __name__ == '__main__':
    # Parameter 
    path_root = r'C:\File_Source_Saved'
    path_m = r'M:\Back_up'


    
    copy_file1 = CopyFile()

    path_folder_local = copy_file1.get_path_folder(path_root)
    path_folder_driver = copy_file1.get_path_folder(path_m)


    while(True):
        print(path_folder_local)
        print(path_folder_driver)

        check_all_object_after_copy = True
        list_folder,_ = compare_value(path_folder_local,path_folder_driver)
        print('main', list_folder)
        copy_processing(list_folder)

        print('repare check copy complete')
        check_copy_complete = copy_processing(list_folder,check_all_object_after_copy)
        if check_copy_complete:
            print('All file in local are copied---> repare to remove folder in local')
            for folder in path_folder_local.keys():
                delete_folder(path_folder_local[folder])
            break
        else:
            print('111111111111111111111111111111111111111111111')
            break


    # SUCCESS = 0
    # src = r'C:\File_Source_Saved_01\MR_USA'
    # dst = r'M:\Test\MR_NICHE'
    
    # cmd = 'rmdir /s '+ src + ' /Q'
    # print(cmd)
    # if  os.system(cmd) == SUCCESS:
    #     print('copy to successful')
    # else:
    #     print('Copy file to failed, please check again')

    # # cmd = 'xcopy '+ src +' '+dst + ' /e /i'


