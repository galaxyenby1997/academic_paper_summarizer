
# ---------------------- Import Flask and flask files ---------------------
from flask import Flask, request, render_template, url_for, redirect, flash
from forms import InputData
from summarization_model import * 



# ------------------------------ App Construction ------------------------------ 




#app init---------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cccc8e72ff5a6a94b2a1483ee18ab3a9'

# main code below -----------------
data = None

@app.route("/")
def home():
	return render_template('homepage.html')




@app.route("/about")
def about():
	return render_template('aboutpage.html')





@app.route("/summarizer", methods=['GET', 'POST'])
def summarizer():
	global data
	data = InputData()
	if data.validate_on_submit():
		flash('Summary is being created! Click the Summarize button again and wait for a few seconds...', 'success')
		return redirect(url_for('prediction'))
	#else:
	#	flash('Information entered is of invalid form! Please try again.')

	#return render_template('input_data.html', title='Summarize your Paper!', form=data)
	return render_template('input_data.html', form=data)





@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
	if request.method == 'POST':
		website = request.form['url_link']
		count = int(request.form['word_count'])
		percent = 0.05

		try:
			paper_html = requests.get(website)
		except:
			message = 'Error: your URL page does not exist or there was a bad connection, or a typo. Please try again.'
		return tuple([message, 'No keywords available'])


		Pair = Summarize_paper(paper_html, count, percent)
		summary = Pair[0]
		keywords = Pair[1]

		if 'Error' in summary: 
			return render_template('prediction_page.html', title='402 Not Found ', summary=summary, keywords=keywords)

		if len(summary) < count:
			warn_message = 'Your word count is too small to generate a informative summary. Please try a larger word count.'
			key_msg = 'No keywords available' 
			return render_template('prediction_page.html', title='Warning: ', summary=warn_message, keywords=key_msg)

		return render_template('prediction_page.html', title='Summary of Paper: ', summary=summary, keywords=keywords)

	return render_template('input_data.html', title='Summarize your Paper!', form=data)
	





# --------- added code below ---------------

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)

	
