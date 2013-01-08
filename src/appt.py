import re
import subprocess
import zipfile
import os
import sys


def get_packageinfo(s):
	d = {}
	for ss in s.split(" "):
		if ss.startswith('name='):
			d['name'] = re.compile(r"'.+'").findall(ss)[0][1:-1]
		elif ss.startswith('versionCode'):
			d['versionCode'] = ss[13:-1]
		elif ss.startswith('versionName'):
			d['versionName'] = ss[13:-1]
	return d

def get_info(sq):
	info = {}
	for ss in sq:
		if ss.strip().startswith('package'):
			info.update(get_packageinfo(ss))
		elif ss.strip().startswith('application-label:'):
		    info['lable'] = ss[19:-1]
		elif ss.strip().startswith('application-label-zh:'):
		    info['lable-zh'] = ss[22:-1]
		elif ss.strip() == 'application-icon:':
		    info['icon'] = ss[18:-1]
		elif ss.strip().startswith('application-icon-120:'):
		    info['icon'] = ss[22:-1]
		elif ss.strip().startswith('application-icon-160:'):
		    info['icon'] = ss[22:-1]
	return info

def get_apkinfo(apk_file):
	proc = subprocess.Popen('aapt d badging "'+apk_file+'" | grep -E "package|application-label|application-icon"',shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	sq = []
	for line in proc.stdout:
		sq = sq + [line.rstrip()]
	info = get_info(sq)
	return info

def get_name(info):
	# return info.get('name','')
	# return "-".join([info.get('name',''), info.get('lable',''), info.get('lable-zh','')])
	return "-".join([info.get('lable',''), info.get('lable-zh',''), info.get('versionName',''),info.get('name','')])
	

def archive_apk(apk_file):

	directory, filename = os.path.split(apk_file)

	# print 'rename s: '+ filename
	info = get_apkinfo(apk_file)
	newname = get_name(info)
	if newname == "": 
		print info
		print apk_file
		return
	newpath = directory + '/' + newname+'.apk' 
	os.rename(apk_file, newpath)
	# print 'rename e: ' + newname

	# save icon
	# print 'icon s: '+ newname
	try:
		f = zipfile.ZipFile(newpath)
		tmpiconpath = f.extract(info.get('icon',''), '/tmp')
		# os.rename(tmpiconpath, directory + '/' + newname + '.png')
		subprocess.check_call(['mv', tmpiconpath, directory + '/' + newname + '.png'])
	except:
		raise
		print 'icon error for %s'%newname
	# print 'icon e: '+ newname
	# print '________'

def archive_dir(apk_dir):
	filelist = os.listdir(apk_dir)
	for f in filelist:
		if f.endswith('.apk'):
			path = apk_dir + '/' + f
			print "process apk %s"%path
			try:
				archive_apk(path)
			except:
				pass

def main():
	if(len(sys.argv) <= 1 ):
		print "pls enter path"
	else:
		archive_dir(sys.argv[1]) 

if __name__=="__main__":
	main()









	