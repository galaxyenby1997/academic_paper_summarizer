# academic_paper_summarizer
Blueprint for a webapp to summarize academic research papers!

This is a blueprint for a webapp (deployed through Heroku probably, using Python's Flask web app framework) that summarizes academic papers
and provides important keywords to google separately, related to the paper's topic. Right now, it only works locally on a machine, but I'm working to get it deployed to the cloud through Heroku or google cloud plaform.

It runs on the Flask framework interface, and
under the hood, uses a unsupervised machine learning algorithm to summarize text based on finding the most important and relevant
sentences. THe algorithm can be downloaded through a library called Gensim, and it's very easy to use since its built into Gensim's
methods. For now, the software summarizes the whole paper, but since academic papers usually are divided into sections, I'm working on having
the software recognize different font (since the heading for each section in a paper, like "Introduction", "Metholodolgy", "Results' is all
written differently from the body of the text) so that the app can summarize BY section, and then integrate the summaries together so the 
information flows more smoothly!
