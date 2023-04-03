from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from .models import Past
from django.core.paginator import Paginator 

# Create Homepage
def home(request):
    # Check for form submission
    if request.method == "POST":
        question = request.POST['question']
        past_responses = request.POST['past_responses']



        #API KEY :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
        #Do API Stuff
        #Set API Key

        openai.api_key = "yourAPI"

        # Create OpenAI Instance
        openai.Model.list()
        try:            
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

            # Logic for past responses
            if "41elder41" in past_responses:
                past_responses = response
            else:
                past_responses = f"{past_responses}<br/><br/>{response}"

                # Save To Database
                record = Past(question=question, answer=response)
                record.save()

            return render(request, 'home.html', {"question":question, "response":response, "past_responses":past_responses})
        
        except Exception as e:
            return render(request, 'home.html', {"question":question, "response":e, "past_responses":past_responses})
    
    return render(request, 'home.html', {})



def past(request):
    #Set up Paginator
    p = Paginator(Past.objects.all(), 5)
    page = request.GET.get('page')
    pages = p.get_page(page)
    
    # Queried The Database
    past = Past.objects.all()

    return render(request, 'past.html', {"past":past, "pages":pages})

def delete_past(request, Past_id):
    past = Past.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, ("That Question and Answer have been deleted..."))
    return redirect('past')
