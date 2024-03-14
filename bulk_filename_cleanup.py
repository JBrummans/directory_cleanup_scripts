# This script parses a folder structure and removes junk spaces and new line characters from filenames
# Was created to cleanup the naming of thousands of department files

import os
import argparse

def find_files_with_space_start(directory):
    file_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.isfile(root+"/.~lock."+file+"#") or "~lock" in file:
                file_list.append(f"File locked skipped,{root}/{file}")
                print("File locked skipping,"+root+"/"+file)
                continue
            try:
               if file.startswith(' '):
                   file_list.append("Leading space,"+os.path.join(root, file))
                   print("leading,"+root+"/"+file+","+root+"/"+file[1:])
                   os.rename(root+"/"+file,root+"/"+file[1:])
                   continue
               if file.endswith(' '):
                   file_list.append("Trailing space,"+os.path.join(root, file))
                   print("trailing,"+root+file+","+root+file[:-1])
                   os.rename(root+"/"+file,root+"/"+file[:-1])
                   continue
               if ' .' in file:
                   file_list.append("Leading space before extension,"+os.path.join(root, file))
                   print("leading extension,"+root+"/"+file+","+root+"/"+file.replace(' .','.'))
                   os.rename(root+"/"+file,root+"/"+file.replace(' .','.'))
                   continue
               if '\n' in file:
                   file_list.append("Newline Character,"+os.path.join(root, file.replace("\n","NEWLINE")))
                   print("Newline,"+root+"/"+file.replace("\n","NEWLINE")+","+root+"/"+file.replace("\n",""))
                   os.rename(root+"/"+file,root+"/"+file.replace("\n",""))
                   continue
            except:
               print(f"failed to write the file, {root}/{file}")

    return file_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find files with spaces at the start of their names.")
    parser.add_argument("directory", nargs='?', default='.', help="Directory to search (default: current directory)")
    args = parser.parse_args()

    input("WARNING FILES WILL BE RENAMED!! Press Enter to continue...")
    print("")
    target_directory = args.directory
    fileslist = find_files_with_space_start(target_directory)
    print("Finished. Number of files: "+ str(len(fileslist)))