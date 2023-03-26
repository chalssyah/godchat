from django.shortcuts import render
import openai

# Create Homepage
def home(request):
    # Check for form submission
    if request.method == "POST":
        question = request.POST['question']

        #Do API Stuff
        #Set API Key
        openai.api_key = "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"
        # Create OpenAI Instance
        openai.Model.list()
        #Make a Completion
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )

        #Parse the response
        response = (response["choices"][0]["text"]).strip()

        return render(request, 'home.html', {"question":question, "response":response})
    
    return render(request, 'home.html', {})
