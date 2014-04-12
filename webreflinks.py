import webapp2
from google.appengine.api import urlfetch
def getAllNewLinksOnPage(temp,page):
	response = urlfetch.fetch(page)
	html = response.content
		
	links=[]
	pos=0
	allFound=False
	count=0
	while not allFound:
		aTag=html.find("<a href=",pos)
		if aTag>-1:
			href=html.find('"',aTag+1)
			endHref=html.find('"',href+1)
			url=html[href+1:endHref]
			fb=url.find('facebook')
			tw=url.find('twitter')
			link=url.find('linkedin')
			'''print(fb," ",tw," ",link," ",blog)'''
			'''inst=url.find('instagram')'''
			'''pint=url.find('pinterest')'''
			if url[:7]=="http://" or url[:8]=="https://" :
				if url[-1]=="/":
					url=url[:-1]
				if not url in links :
					'''and fb==-1 and tw==-1 and link==-1'''
					count=count+1
					temp.write('\r\n')
					temp.write(count)
					temp.write(' :\t')
					temp.write(url)
					links.append(url)
			closeTag=html.find("</a>",aTag)
			pos=closeTag+1
		else:
			allFound=True
	return links

class FormPage(webapp2.RequestHandler):
	def get(self):
		html="""\
		<html><head><title>Link Map Generator</title></head><body>
		<div align="center">
		<form align="center" action="/list" method="post">
		<input type="url" name="content" value="http://computingfreak.org" size="80">
		<input type="submit" name="sub" value="list">
		</form>
		<br/><br/><br/>
		Use <a href="/api">this</a> to use this service as an API via GET calls.
		the URL must be passed as the value of the parameter 'content'
		<br/>The above form uses POST to send data to the server at <b>/list</b>.
		The Get-Ready API is hosted at <b>/api</b>.
		</div>
		</body></html>"""
		self.response.write(html)
		
class PostPage(webapp2.RequestHandler):
	def get(self):
		'''Redirect to Home Page on User attempting a GET request directly without sending POST parameters'''
		self.redirect("/")
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello World')
		self.response.out.write('\r\n')
		self.response.write('Seed URL : ')
		seed=self.request.get('content')
		self.response.write(seed)
		self.response.out.write('\r\n')
		result = urlfetch.fetch(seed)
		'''self.response.write(result.content)'''
		toCrawl=[seed]
		crawled=[]
		while toCrawl:
			url=toCrawl.pop()
			crawled.append(url)
			newLinks=getAllNewLinksOnPage(self.response,url)
		'''self.response.write(crawled)'''
		self.response.out.write('\r\n\r\n')
		self.response.write('Bye World')

class GetPage(webapp2.RequestHandler):
	def get(self):
		'''GET Style - API for other web/standalone services/applications'''
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello World')
		self.response.out.write('\r\n')
		
		seed=self.request.get('content')
		if len(seed)<5 :
			self.response.write('MalformedURL Exception - using default')
			seed="http://computingfreak.org"
		else :
			self.response.write('Seed URL : ')
			self.response.write(seed)
		self.response.out.write('\r\n')
		result = urlfetch.fetch(seed)
		'''self.response.write(result.content)'''
		toCrawl=[seed]
		crawled=[]
		while toCrawl:
			url=toCrawl.pop()
			crawled.append(url)
			newLinks=getAllNewLinksOnPage(self.response,url)
		'''self.response.write(crawled)'''
		self.response.out.write('\r\n\r\n')
		self.response.write('Bye World')
		
application = webapp2.WSGIApplication([('/', FormPage)], debug=True)
list = webapp2.WSGIApplication([('/list', PostPage)])
api = webapp2.WSGIApplication([('/api', GetPage)])

def main():
	application.run()
	list.run()
	api.run()
	
if __name__ == "__main__":
    main()