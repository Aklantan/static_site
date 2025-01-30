import os
import shutil





def copy_static(src,dest):
   if not os.path.exists(src):
      raise Exception ("Source folder not found")
   if os.path.exists(dest):
    shutil.rmtree(dest)
   os.makedirs(dest)
   with os.scandir(src) as entries:
      for entry in entries:
        src_path = os.path.join(src,entry.name)
        dest_path = os.path.join(dest,entry.name)
        if entry.is_file():
           print(entry.path)
           shutil.copy2(src_path,dest_path)
        elif entry.is_dir():
           print(entry.path)
           copy_static(src_path,dest_path)
          
        

