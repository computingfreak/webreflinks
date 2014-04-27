import webapp2
from google.appengine.api import urlfetch
def generateLinks(temp,word):
	links=[]
	ext=["com","org","net","io","sh","in","me","co","mobi","name","info"]
	siteprefix=["facebook.com","twitter.com","flickr.com","instagram.com","pinterest.com","foursquare.com","github.com","notepad.cc"]
	sitesuffix=["tumblr.com","github.io","appspot.com","herokuapp.com","wordpress.com","blogspot.com"]
	linebreak="""<br/>"""
	beginhtml="""<html><head><title>Link Generator</title></head><body>"""
	begindiv="""<div align='center' style='color:black;background-color:white'>"""
	endhtml="""</body></html>"""
	begintable="""<table border='1' width='90%'>"""
	endtable="""</table>"""
	enddiv="""</div>"""
	startheader="""<th>"""
	endheader="""</th>"""
	startrow="""<tr>"""
	endrow="""</tr>"""
	startcell="""<td align="center">"""
	endcell="""</td>"""
	html=""""""
	html=html+beginhtml+begindiv
	
	#domain extensions
	
	html=html+begintable
	
	for c in range(len(ext)):
		html=html+startheader
		html=html+ext[c].upper()
		html=html+endheader
	
	html=html+startrow
	pre="'http://"
	
	for c in range(len(ext)):
		html=html+startcell
		link=pre+word+"."+ext[c]+"'"
		links.append(link)
		html=html+"""<a href="""+link+""">"""+word+"""</a>"""
		html=html+endcell
	
	html=html+endrow
	
	html=html+endtable+enddiv
	
	html=html+linebreak
	
	#prefix domains
	
	html=html+begindiv+begintable
	
	for c in range(len(siteprefix)):
		html=html+startheader
		html=html+siteprefix[c].capitalize()
		html=html+endheader
		
	html=html+startrow
	
	for c in range(len(siteprefix)):
		html=html+startcell
		link=pre+siteprefix[c]+"/"+word+"'"
		links.append(link)
		html=html+"""<a href="""+link+""">"""+word+"""</a>"""
		html=html+endcell
		
	html=html+endrow
	
	html=html+endtable+enddiv
	
	html=html+linebreak
	
	#postfix domains
	
	html=html+begindiv+begintable
	
	for c in range(len(sitesuffix)):
		html=html+startheader
		html=html+sitesuffix[c].capitalize()
		html=html+endheader
		
	html=html+startrow
	
	for c in range(len(sitesuffix)):
		html=html+startcell
		link=pre+word+"."+sitesuffix[c]+"'"
		links.append(link)
		html=html+"""<a href="""+link+""">"""+word+"""</a>"""
		html=html+endcell
		
	html=html+endrow
	
	html=html+endtable+enddiv
	
	html=html+endhtml
	return html
	
def getWebRefLinks(test,page):
	response = urlfetch.fetch(page)
	html = response.content		
	links=[]
	pos=0
	allFound=False
	count=0
	temp="""\
	"""
	current=""
	while not allFound:
		aTag=html.find("<a href=",pos)
		if aTag>-1:
			href=html.find('"',aTag+1)
			endHref=html.find('"',href+1)
			url=html[href+1:endHref]
			#fb=url.find('facebook')
			#tw=url.find('twitter')
			#link=url.find('linkedin')
			#print(fb," ",tw," ",link," ",blog)
			#inst=url.find('instagram')
			#pint=url.find('pinterest')
			if url[:7]=="http://" or url[:8]=="https://" :
				if url[-1]=="/":
					url=url[:-1]
				if not url in links :
					#and fb==-1 and tw==-1 and link==-1
					count=count+1
					links.append(url)
					anchor="""<a href='"""+url+"""'>"""+url+"""</a>"""
					current="<br/>\r\n"+str(count)+" :\t"+anchor
					temp=temp+current
			closeTag=html.find("</a>",aTag)
			pos=closeTag+1
		else:
			allFound=True
	test.write(temp)
	return links

class HomePage(webapp2.RequestHandler):
	def get(self):
		html="""\
		<html><head><title>Welcome Page</title></head><body>
		<div align="center">Please navigate this way to my <a href="http://computingfreak.org">homepage</a>.</div>
		<div>Or check my other projects at<br/>
		<ul>
		<li><a href="/webreflinks">WebRefLinks Tool</a></li>
		<li><a href="/domgen">DomGen Tool</a></li>
		</ul>
		</div>
		<div>Here are some hyperlinks that give you a glance at my social activity. Check <a href="http://klout.com/computingfreak">Klout</a><br/>
		<ol>
		<li><a href="http://facebook.com/computingfreak">Facebook</a></li>
		<li><a href="http://twitter.com/computingfreak">Twitter</a></li>
		<li><a href="http://linkedin.com/in/computingfreak">LinkedIn</a></li>
		<li><a href="http://flickr.com/computingfreak">Flickr</a></li>
		<li><a href="http://computingfreak.tumblr.com/">Tumblr</a></li>
		<li><a href="http://instagram.com/computingfreak">Instagram</a></li>
		<li><a href="http://pinterest.com/computingfreak">Pinterest</a></li>
		<li><a href="http://foursquare.com/computingfreak">FourSquare</a></li>
		<li><a href="http://github.com/computingfreak">GitHub</a></li>
		<li><a href="http://storify.com/computingfreak">Storify</a></li>
		<li><a href="http://angel.co/computingfreak">Angel</a></li>
		<li><a href="http://geekli.st/computingfreak">GeekList</a></li>
		</ol>
		</div>
		</body></html>"""
		self.response.write(html)
		
class WebRefLinksFormPage(webapp2.RequestHandler):
	def get(self):
		html="""\
		<html><head><title>Link Map Generator</title></head><body>
		<div align="center">
		<form align="center" action="/webrefpost" method="post">
		<input type="url" name="content" value="http://computingfreak.org" size="80">
		<input type="submit" name="sub" value="list">
		</form>
		<br/><br/><br/>
		Use <a href="/webrefget">this</a> to use this service as an API via GET calls.
		the URL must be passed as the value of the parameter 'content'
		<br/>The above form uses POST to send data to the server at <b>/webrefpost</b>.
		The Get-Ready API is hosted at <b>/webrefget</b>.
		</div>
		</body></html>"""
		self.response.write(html)

class DomGenFormPage(webapp2.RequestHandler):
	def get(self):
		html="""\
		<html><head><title>Link Generator</title></head><body>
		<div align="center">
		<form align="center" action="/domgenpost" method="post">
		<input type="text" name="content" value="computingfreak" size="80">
		<input type="submit" name="sub" value="list">
		</form>
		<br/><br/><br/>
		Use <a href="/domgenget">this</a> to use this service as an API via GET calls.
		the keyword must be passed as the value of the parameter 'content'
		<br/>The above form uses POST to generate links the server at <b>/domgenpost</b>.
		The Get-Ready API is hosted at <b>/domgenget</b>.
		</div>
		</body></html>"""
		self.response.write(html)
		
class WebRefLinksPostPage(webapp2.RequestHandler):
	def get(self):
		'''Redirect to Home Page on User attempting a GET request directly without sending POST parameters'''
		self.redirect("/webreflinks")
	def post(self):
		#self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello World')
		self.response.out.write('\r\n<br/>\r\n')
		self.response.write('Seed URL : ')
		seed=self.request.get('content')
		self.response.write(seed)
		self.response.out.write('\r\n<br/>\r\n')
		result = urlfetch.fetch(seed)
		#self.response.write(result.content)
		toCrawl=[seed]
		crawled=[]
		while toCrawl:
			url=toCrawl.pop()
			crawled.append(url)
			newLinks=getWebRefLinks(self.response,url)
			print(newLinks)
		#self.response.write(crawled)
		self.response.out.write('\r\n<br/>\r\n')
		self.response.write('Bye World')

class WebRefLinksGetPage(webapp2.RequestHandler):
	def get(self):
		'''GET Style - API for other web/standalone services/applications'''
		#self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello World')
		self.response.out.write('\r\n<br/>\r\n')
		
		seed=self.request.get('content')
		if len(seed)<5 :
			self.response.write('MalformedURL Exception - using default')
			seed="http://computingfreak.org"
		else :
			self.response.write('Seed URL : ')
			self.response.write(seed)
		self.response.out.write('\r\n<br/>\r\n')
		result = urlfetch.fetch(seed)
		#self.response.write(result.content)
		toCrawl=[seed]
		crawled=[]
		while toCrawl:
			url=toCrawl.pop()
			crawled.append(url)
			newLinks=getWebRefLinks(self.response,url)
			print(newLinks)
		#self.response.write(crawled)
		self.response.out.write('\r\n<br/>\r\n')
		self.response.write('Bye World')
		
class DomGenPostPage(webapp2.RequestHandler):
	def get(self):
		'''Redirect to Home Page on User attempting a GET request directly without sending POST parameters'''
		self.redirect("/domgen")
	def post(self):
		#self.response.headers['Content-Type'] = 'text/plain'
		#self.response.write('Hello World')
		self.response.out.write('\r\n<br/>\r\n')
		#self.response.write('Seed keyword : ')
		seed=self.request.get('content')
		#self.response.write(seed)
		self.response.out.write('\r\n<br/>\r\n')
		text=generateLinks(self.response,seed)
		print(text)
		self.response.write(text)
		self.response.out.write('\r\n<br/>\r\n')
		#self.response.write('Bye World')

class DomGenGetPage(webapp2.RequestHandler):
	def get(self):
		'''GET Style - API for other web/standalone services/applications'''
		#self.response.headers['Content-Type'] = 'text/plain'
		#self.response.write('Hello World')
		self.response.out.write('\r\n<br/>\r\n')
		#self.response.write('Seed keyword : ')
		seed=self.request.get('content')
		if len(seed)<2 :
			self.response.write('Keyword too short, using default')
			seed="computingfreak"
		else :
			#self.response.write('Seed keyword : ')
			#self.response.write(seed)
			pass
		self.response.out.write('\r\n<br/>\r\n')
		text=generateLinks(self.response,seed)
		print(text)
		self.response.write(text)
		self.response.out.write('\r\n<br/>\r\n')
		#self.response.write('Bye World')
		
home = webapp2.WSGIApplication([('/', HomePage)], debug=True)
webref = webapp2.WSGIApplication([('/webreflinks', WebRefLinksFormPage)], debug=True)
domgen = webapp2.WSGIApplication([('/domgen', DomGenFormPage)], debug=True)
webrefpost = webapp2.WSGIApplication([('/webrefpost', WebRefLinksPostPage)], debug=True)
webrefget = webapp2.WSGIApplication([('/webrefget', WebRefLinksGetPage)], debug=True)
domgenpost = webapp2.WSGIApplication([('/domgenpost', DomGenPostPage)], debug=True)
domgenget = webapp2.WSGIApplication([('/domgenget', DomGenGetPage)], debug=True)

def main():
	home.run()
	webref.run()
	webrefpost.run()
	webrefget.run()
	domgen.run()
	domgenpost.run()
	domgenget.run()
	
if __name__ == "__main__":
    main()
