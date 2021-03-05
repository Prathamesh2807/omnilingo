import re 
import jieba
import thai_segmenter
import nagisa

def bre(sentence):
	"""
		tokenise.tokenise("Tennañ a rit da'm c'hoar.", lang="bre")
		['Tennañ', 'a', 'rit', 'da', "'m", "c'hoar", '.']
	"""
	o = sentence
	o = o.replace("c'h", "cʼh")
	o = o.replace("C'h", "Cʼh")
	o = o.replace("C'H", "CʼH")
	o = re.sub("([!%()*+,\./:;=>?«»–‘’“”…€½]+)", " \g<1> ", o)
	o = re.sub("'", " '", o)
	o = re.sub("  *", " ", o)

	return [i.replace("ʼ", "'") for i in o.split(" ") if not i.strip() == "" ]

def tur(sentence):
	"""
		tokenise.tokenise("İlk Balkan Schengen'i mi?", lang="tur")
		['İlk', 'Balkan', "Schengen'i", 'mi', '?']
	"""
	o = re.sub("'", "ʼ", sentence)

	return [i.replace("ʼ", "'") for i in re.split("(\\w+)", o) if not i.strip() == "" ]


def hin(sentence):
	"""
		tokenisers.tokenise("हिट एंड रन केस: भाग्यश्री के खिलाफ भी सलमान खान जैसी शिकायत!", lang="hin")
		['हिट', 'एंड', 'रन', 'केस', ':', 'भाग्यश्री', 'के', 'खिलाफ', 'भी', 'सलमान', 'खान', 'जैसी', 'शिकायत', '!']
		NOTE: not using \w as it won't match certain Devanagari chars.
		FIXME: Improve this, 
	"""
	o = sentence
	o = re.sub("([!&,-.:?|।‘]+)", " \g<1> ", o)
	o = re.sub('"', ' " ', o)
	o = re.sub("'", " ' ", o)
	o = re.sub("  *", " ", o)

	return [ x for x in re.split(" ", o) if not x.strip() == "" ]

def default(sentence):
        return [ x for x in re.split("(\\w+)", sentence) if x.strip() ]

def tokenise(sentence, lang):
	if lang in ["br", "bre"]:
		return bre(sentence)
	if lang in ["tr", "tur"]:
		return tur(sentence)
	if lang in ["hi", "hin"]:
		return hin(sentence)
	if lang in ["zh", "zho"] or lang.startswith("zh-"):
	        return jieba.lcut(sentence)
	if lang in ["th", "tha"]:
	        return thai_segmenter.tokenize(sentence)
	if lang in ["ja", "jpn"]:
		"""
			tokenisers.tokenise("自然消滅することは目に見えてるじゃん。", lang="jpn")
			['自然', '消滅', 'する', 'こと', 'は', '目', 'に', '見え', 'てる', 'じゃん', '。']
		"""
		return nagisa.tagging(sentence).words
	else:
		return default(sentence)