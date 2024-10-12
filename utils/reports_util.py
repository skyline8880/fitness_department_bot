import os

def set_path(filename):
    return f"./report_dir/output/{filename}" 
    reports_dir = "reports_dir"
    full_path = os.path.join(os.getcwd(), reports_dir, filename)
    return full_path

#  from reports_util import set_path
#  def send_document(file_path):
#####  for example ####
#  report_path = set_path(filename)
#  send_document(report_path)
#
#
#
#
#
#
#
