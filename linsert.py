import sys
import os

exclude_directories = ["dependencies", "packages"]

available_licenses = ["gnu_3.0"]

gnu30_notice = "// This file is part of {project_name}.\n//\n// {project_name} is free software: you can redistribute it and/or modify\n// it under the terms of the GNU General Public License as published by\n// the Free Software Foundation, either version 3 of the License, or\n// (at your option) any later version.\n//\n// {project_name} is distributed in the hope that it will be useful,\n// but WITHOUT ANY WARRANTY; without even the implied warranty of\n// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n// GNU General Public License for more details.\n//\n// You should have received a copy of the GNU General Public License\n// along with {project_name}.  If not, see <https://www.gnu.org/licenses/>."

def validate_args(args):
  if len(args) < 4:
    return False
  if args[1] not in available_licenses:
    return False
  if os.path.exists(args[3]) == False:
    return False
  return True

def retrieve_filenames(path, exclude):
  result = []
  for root, dirs, files in os.walk(path):
    dirs[:] = [d for d in dirs if d not in exclude]
    for file in files:
      if file.endswith(tuple([".c", ".cpp", ".h", ".hpp"])):
        result.append(os.path.join(root, file))
  return result

def choose_license_notice(license):
  if license == "gnu_3.0":
    return gnu30_notice

def main():
  if validate_args(sys.argv):
    project_name = sys.argv[2]
    license_notice = choose_license_notice(sys.argv[1]).format(project_name = project_name)
    root_path = sys.argv[3]
    files = retrieve_filenames(root_path, exclude_directories)
    files_w = []
    files_wo = []
    for file in files:
      if license_notice in open(file).read():
        files_w.append(file)
      else:
        files_wo.append(file)
    if len(files_wo) != 0:
      print("Following files don't have provided license\nnotice (or it doesn't match with template).\n")
      for file in files_wo:
        print(file)
      sure = input("\nFiles listed above will be modified. Are you sure? [yes]: ")
      if (sure == "yes"):
        for file in files_wo:
          with open(file, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(license_notice.rstrip('\r\n') + '\n\n' + content)
  else:
    print("Invalid arguments list provided")

if __name__ == "__main__":
  main()
