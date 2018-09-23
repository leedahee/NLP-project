import xml.etree.ElementTree as ET
import re
import os
import glob
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer 



class LazyDict(dict):
    def keylist(self, keys, value):
        for key in keys:
            self[key] = value

def split_semi(sent):
	no_semi = sent.split(';')
	return no_semi

def split_colon(sent):
	no_colon = sent.split(':')
	return no_colon

def split_space(sent):
	sent_list = sent.split(" ")
	return sent_list

def stemming(strings):
	small_list = small.split(" ")
	porter = nltk.PorterStemmer()
	stemed_list = [porter.stem(small) for small in small_list]
	return stemed_list

def noPeriodSentList(sent_list):
	# print ('function')
	# print (sent_list)
	if len(sent_list[-1])>1:
		if sent_list[-1][-1]=='.':
			sent_list[-1] = sent_list[-1][:-1]
	return sent_list

def checkNegation(sent_list, tag):
	# print (stemed_list)
	n=0
	ind = sent_list.index(tag)
	negations = ['no','deny','denies','denied','not','negative','-']
	# if file_number=='389':
	for negation in negations:
		# print (sent_list[:ind+3])
		if negation in sent_list[:ind+3]:
			n=-1

	affirm= ['although', '+']
	for a in affirm:
		if a in sent_list[:ind]:
			n=n+1
	return n

def checkPurpose(sent_list, tag):
	p=0
	ind = sent_list.index(tag)
	if 'for' in sent_list[ind:]:
		p=-1
	return p


def checkNegative(sent_list, tag):
	t=0
	ind = sent_list.index(tag)
	if 'negative' in sent_list[ind:]:
		t=-1
	return t

#  ================================= Tag dictionary ================================== 

tag_dic = LazyDict()
tag_dic.keylist(('marijuana', 'cocaine','heroin','IVDU', 'IV'), 'MCHTAG')
tag_dic.keylist(('drug','substance'), 'SUBTAG')
tag_dic.keylist(('previous(ly)?', 'past', '(in the )? past', 'occasional(ly)?','ago','recent(ly)?'),'STATUSTAG')
tag_dic.keylist(('-'), ' - ')
tag_dic.keylist(('+'), ' + ')

tag_dic.keylist(('illicit', 'psychedelic', 'recreational'),'ADJTAG')
tag_dic.keylist(('history( of)?','h\/o'),'HISTORYTAG')
# tag_dic.keylist(('has used','(abused?s?)','use of', '\suse[a-zA-Z]*', 'smoking'),' USETAG')


# # ================================= Generating tagged file ================================== 
# file_name = ['126.xml', '157.xml','159.xml', '169.xml', '184.xml', '210.xml', '215.xml', '325.xml', '338.xml', '356.xml', '381.xml','382.xml']

con_dic ={}
mch_dic ={}
adj_dic={}

with open('/Users/daheelee/Desktop/tagged2/result.csv','w') as regex_csv:
	writer = csv.DictWriter(regex_csv, fieldnames=['file','small','mchtag','ADJ_SUB','conclusion','met'])
	writer.writeheader()

	path = '/Users/daheelee/Desktop/train'
	for f in glob.glob(os.path.join(path, '*.xml')):
	# for f in file_name:

	# f= '126.xml'
		tree=ET.parse(f)
		root=tree.getroot()
		contents = root[0].text
		yesorno = root[1][6].get('met')
		
		rule_dic={}
		if yesorno =='met':
			rule_dic['met']='met'
		else :
			rule_dic['met']=''

		for i,j in tag_dic.items():	
			if (i=='+'):
				i = "\+"
			contents = re.sub(i,j,contents.lower())
		

		file_number = os.path.splitext(os.path.basename(f))[0]
		rule_dic['file']=file_number
		writer.writerow(rule_dic)

		
		sentences = nltk.sent_tokenize(contents)
		# if file_number=='397':
		for sentence in sentences:
			no_colons = split_colon(sentence)
			# print ('==========',file_number,'===============')
			# print (no_colon)
			# if file_number=='159':
			for no_colon in no_colons:
				if 'mchtag' in no_colon:
					# print ('yes')
					no_semies = split_semi(no_colon)
					no_semies = noPeriodSentList(no_semies)

					# print ('==========',file_number,'===============')
					# print (no_semies)
					for no_semi in no_semies:
						sent_list = split_space(no_semi)
						if 'mchtag' in sent_list:
							print ('=========MCTTAG=',file_number,'===============')
							print (sent_list)
							n=checkNegation(sent_list,'mchtag')
							n=1+n
							p=checkPurpose(sent_list,'mchtag')
							p=1+p
							# print (n,p)

							if n+p == 1:
								conclusion_mch = 'unmet'
							else:
								conclusion_mch ='met'
							
							if file_number not in mch_dic.keys():
								mch_dic[file_number] = conclusion_mch

							# print ('=========MCTTAG=',file_number,'===============')
							print (conclusion_mch)

							# # ## Final dictionary
							# # con_dic['mchtag'][no_semi] = n
							# # con_dic['mchtag']['purpose']
							## Write CSV
							# rule_dic['file'] =file_number
							# rule_dic['small'] = no_semi
							# rule_dic['mchtag'] = n
							# rule_dic['conclusion'] = conclusion
						# writer.writerow(rule_dic)

				if 'adjtag subtag' in no_colon:
					no_semies = split_semi(no_colon)
					no_semies = noPeriodSentList(no_semies)
					# print ('==========',file_number,'===============')
					# print (no_semies)
					for no_semi in no_semies:
						sent_list = split_space(no_semi)
						if 'adjtag' in sent_list:
							# if file_number=='365':
							print ('====ADJTAG======',file_number,'===============')
							print (sent_list)
							n=checkNegation(sent_list,'adjtag')
							n=1+n
							p=checkPurpose(sent_list,'adjtag')
							p=1+p
						
							if n+p == 1:
								conclusion_adj = 'unmet'
							else:
								conclusion_adj ='met'
							# print (n,p)
							# print ('====ADJTAG======',file_number,'===============')
							print (conclusion_adj)

							# print (conclusion)
							if file_number not in adj_dic.keys():
								adj_dic[file_number] = conclusion_adj

print (adj_dic)
print (mch_dic)

# class Conclusion(a,b):
# 	def __init__(self):
# 		self.file_number=a
# 		self.conclusion =b

# if Conclusion.file_number


					# 	# ## Final dictionary
# 					# 	# con_dic['mchtag'][no_semi] = n
# 					# 	# con_dic['mchtag']['purpose']
# 					## Write CSV
# 					rule_dic['file'] =file_number
# 					rule_dic['small'] = no_semi
# 					# rule_dic['ADJ_SUB'] = n
# 					# rule_dic['conclusion'] = conclusion
# 					# rule_dic['purpose'] =p
# 				writer.writerow(rule_dic)






# # 	file_number = os.path.splitext(os.path.basename(f))[0]
# # 	tagged_file = file_number+'_tagged'
# # 	os.path.expanduser("~/Desktop/somedir/somefile.txt")
# # 	with open('/Users/daheelee/Desktop/tagged/'+str(tagged_file)+'.txt','w') as f:
# # 		f.write(contents)
# # # # ======================================= rule =========================================
# # # # ================================ rul1 : successive tag ================================

# # rule1 = 'HISTORYTAG STATUSTAG ADJTAG drug USETAG'
# # vectorizer = CountVectorizer(ngram_range=(1,6))
# # analyzer = vectorizer.build_analyzer()
# # combination = analyzer(rule1)

# # rule2 = '(HISTORYTAG )?(STATUSTAG )?(ADJTAG ?\/? )+(drug |DRUGTAG )+(USETAG )?'

# # r126 = 'HISTORYTAG STATUSTAG ADJTAG drug USETAG'
# # r157 = 'STATUSTAG HISTORYTAG ADJTAG/ADJTAG drug USETAG'
# # r159 = 'HISTORYTAG DRUGTAG USETAG'
# # r169 = 'STATUSTAG DRUGTAG'
# # r184 = 'DRUGTAG USETAG'
# # r210 = 'HISTORYTAG drug USETAG'
# # r215 = 'HISTORYTAG DRUGTAG'
# # r325 = 'STATUSTAG USETAG DRUGTAG'
# # r356 = 'USETAG DRUGTAG'
# # r381 = 'USETAG DRUGTAG HISTORY'
# # rule = [r126, r157, r159,r169,r184,r210,r215,r325,r356,r381]

# # ================================ regex result table ========================================
# # reg_dics =['DRUGTAG']

# # with open('/Users/daheelee/Desktop/tagged2/regex.csv','w') as regex_csv:
# # 	writer = csv.DictWriter(regex_csv, fieldnames=['file']+reg_dics)
# # 	writer.writeheader()


# # 	path = '/Users/daheelee/Desktop/tagged'


# # 	for filename in glob.glob(os.path.join(path, '*.txt')):
# # 		# test_file = '/Users/daheelee/Desktop/tagged/126_tagged.txt'
# # 		f= open(filename,'r')
# # 		fr=f.read()

		
# 		# print (file_number)

# # 		reg_dic={}
# # 		for r in rule: 
# # 			file_number = os.path.splitext(os.path.basename(filename))[0]
# # 			reg_dic['file']=file_number
# # 			cc= re.findall(r,fr)
# # 			reg_dic[r] = len(cc)

# # 		writer.writerow(reg_dic)
# # 	reg_dics.append(reg_dic)
# # # print (reg_dics)





# # ================================ n-gram result table ======================================== 
# # open tagged file

# with open('/Users/daheelee/Desktop/tagged/ngram.csv','w') as ngram_csv:
# 	writer = csv.DictWriter(ngram_csv, fieldnames=['file']+combination)
# 	writer.writeheader()

# 	path = '/Users/daheelee/Desktop/tagged'


# 	for filename in glob.glob(os.path.join(path, '*.txt')):
# 		f= open(filename,'r')
# 		fr=f.read()
# 		file_number = os.path.splitext(os.path.basename(filename))[0]

# 		di = {}
# 		for c in combination: 
# 			find = re.findall(c,fr,re.I)
# 			di['file'] = file_number
# 			di[c] = len(find)
# 		print(di)

# 		writer.writerow(di)







