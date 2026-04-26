from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SnippetForm
from django.contrib.auth.models import User
from .models import Language

#    TODO: Implement this class to handle snippet creation, only for authenticated users.
#*   RESOLVED!
class SnippetAdd(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, "snippets/snippet_add.html", {"form": SnippetForm(), "action": "Add Snippet"})
        else:
            return redirect("login")
    
    def post(self, request, *args, **kwargs):
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect("index")
        else:
            return redirect("add_snippet")

#    TODO: Implement this class to handle snippet editing. Allow editing only for the owner.
#*   RESOLVED!
class SnippetEdit(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            snippet_id = self.kwargs["id"]
            snippet = Snippet.objects.get(id=snippet_id)
            
            if snippet.user == request.user:
                form = SnippetForm(instance=snippet)
                return render(request, "snippets/snippet_add.html", {"form": form, "action": "Edit Snippet"})
            else:
                return redirect("index")
        else:
            return redirect("index")
    
    def post(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        snippet = Snippet.objects.get(id=snippet_id)
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            return render(request, "snippets/snippet_add.html")

#    TODO: Implement this class to handle snippet deletion. Allow deletion only for the owner.
#*   RESOLVED!
class SnippetDelete(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            snippet_id = self.kwargs["id"]
            snippet = Snippet.objects.get(id=snippet_id)
            
            if snippet.user == request.user:
                form = SnippetForm(instance=snippet)
                return render(request, "snippets/snippet_add.html", {"form": form, "action": "Delete Snippet"})
            else:
                return redirect("index")
        else:
            return redirect("index")
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            snippet_id = self.kwargs["id"]
            snippet = Snippet.objects.get(id=snippet_id)

            if snippet.user == request.user:
                snippet.delete()
                return redirect("index")
            else:
                return redirect("index")
        else:
            return redirect("index")

class SnippetDetails(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        # TODO: Implement logic to get snippet by ID
        #*   RESOLVED!
        if request.user.is_authenticated:
            snippet = Snippet.objects.filter(Q(id=snippet_id) & (Q(public=True) | Q(user=request.user)))
            if not snippet:
                return redirect("index")
        else:
            snippet = Snippet.objects.filter(id=snippet_id, public=True)
            if not snippet:
                return redirect("index")
        
        # Add conditions for private snippets
        return render(
            request, "snippets/snippet.html", {"snippet": snippet}
        )  # Placeholder

class UserSnippets(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        # TODO: Fetch user snippets based on username and public/private logic
        #*   RESOLVED!
        user_id = User.objects.get(username=username).id
        if request.user.is_authenticated and request.user.id == user_id:
            snippets = Snippet.objects.filter(user=user_id)
        else:
            snippets = Snippet.objects.filter(user=user_id, public=True)
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": snippets},
        )  # Placeholder


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        language_id = Language.objects.get(slug=language).id
        # TODO: Fetch snippets based on language
        #*   RESOLVED!
        if request.user.is_authenticated:
            snippets = Snippet.objects.filter(Q(language=language_id) & (Q(public=True) | Q(user=request.user)))
        else:
            snippets = Snippet.objects.filter(language=language_id, public=True)
        return render(request, "index.html", {"snippets": snippets})  # Placeholder


#    TODO: Implement login view logic with AuthenticationForm and login handling.
#*   RESOLVED!
class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html", {"form": AuthenticationForm()})
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("login exitoso")
            return redirect("index")
        else:
            print("Error")
            return render(request, "login.html", {"form": form})

#    TODO: Implement logout view logic. 
#*   RESOLVED!
class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")

from .models import Snippet
from django.db.models import Q

class Index(View):
    def get(self, request, *args, **kwargs):
        # TODO: Fetch and display all public snippets
        #* RESOLVED!
        if request.user.is_authenticated:
            snippets = Snippet.objects.filter(Q(public=True) | Q(user=request.user))
        else:
            snippets = Snippet.objects.filter(public=True)
        return render(request, "index.html", {"snippets": snippets})
