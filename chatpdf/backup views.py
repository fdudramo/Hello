from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ChatmessageCreateForm, FileUploadForm
from django import forms
from .models import *
from django.http import Http404
from django.core.files.storage import FileSystemStorage
from .process_ai import pdf_to_vector
import os


def home(request):
	return render(request, "home.html", {})


def login_usr(request):
	if request.method== 'POST':
		username= request.POST['username'] 
		email= request.POST['email']
		password= request.POST['password']
		user = authenticate(request, username=username, password=password, email=email)
		if user is not None:
			login(request, user)
			messages.success(request, ('you have login successfully'))
			return redirect('home')

		else:
			messages.success(request, ('there was an error, please try again'))
			return redirect('login')	

	else: return render(request, "login.html", {})	


def logout_usr(request):
	messages.success(request, ('you have logout successfully'))
	logout(request)
	return redirect('home')



def signup_usr(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem signup, please try again..."))
			return redirect('signup')
	else:
		return render(request, 'signup.html', {'form':form})


def reset_password(request):
	return render(request, "reset-password.html", {})		

def overview(request):
	return render(request, "index.html", {})

def settings(request):
	return render(request, "settings.html", {})			

def account(request):
	return render(request, "account.html", {})	

def help(request):
	return render(request, "help.html", {})		

def notification(request):
	return render(request, "notifications.html", {})			

def notfound(request):
	return render(request, "404.html", {})

def start(request):
	return render(request, "start.html", {})
	

@login_required
def docs(request):
	files= UploadedFile.objects.all()
	# files=[]

	# for obj in files_objects:
	# 	obj_name= (obj.file.name).replace('uploads/', '').replace('.png', '')
	# 	obj_type= (obj.file.name)#.split('.')[1].upper()

	# 	#files[obj] = {'name': obj_name, 'type': obj_type}
	# 	files.append(({'name': obj_name, 'type': obj_type}))

	return render(request, "docs.html", {'files':files})	
	

		




@login_required
def app(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    chat_form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
    	if request.user not in chat_group.members.all():
    		raise Http404()

    	for member in chat_group.members.all():
    		if member != request.user:
    			other_user = member
    			break	


    if request.htmx:
        chat_form = ChatmessageCreateForm(request.POST)
        if chat_form.is_valid():
            message = chat_form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message' : message,
                'user' : request.user
            }
            return render(request, 'chat/partials/chat_message_p.html', context)


    context={
    	'chat_messages': chat_messages,
    	'chat_form': chat_form,
    	'other_user' : other_user,
    	'chatroom_name' : chatroom_name,
    	'chat_group' : chat_group,
    }	


    return render(request, "app.html", context)



@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user

            upload_file_vector= str(uploaded_file.file.path).replace('media', 'media\\vector')

            # Check if the vector file already exists
            # if UploadedFile.objects.filter(user=request.user, file=uploaded_file.file.name, vector_file=upload_file_vector , vector_file__isnull=False).exists():
            #     messages.error(request, 'File already exists!', extra_tags='safe')

            if UploadedFile.objects.filter(user=request.user, vector_file=upload_file_vector).exists():
                messages.error(request, 'File already exists!', extra_tags='safe')
            else:
                uploaded_file.save()

                # Process the PDF file
                vector_path = pdf_to_vector(uploaded_file.file.path)
                
                # Save the vector file path to the model
                uploaded_file.vector_file = vector_path
                uploaded_file.save()

                # Delete the actual PDF file but keep the path
                if os.path.exists(uploaded_file.file.path):
                    os.remove(uploaded_file.file.path)

                # Add a success message
                messages.success(request, f'File uploaded and processed successfully!, the path: {uploaded_file.file.name}', extra_tags='safe')
                #messages.success(request, 'File uploaded and processed successfully!', extra_tags='safe')
                
            #return redirect('start-chat')
            return redirect('upload_file')

        else:
            messages.error(request, 'Failed! Please try again.', extra_tags='safe')
            return redirect('upload_file')
    else:
        form = FileUploadForm()
    
    return render(request, 'upload.html', {'form': form})



@login_required
def delete_vector_db(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id, user=request.user)
        
        # Delete the vector file from the filesystem
        # if uploaded_file.vector_file and os.path.exists(uploaded_file.vector_file):
        #     os.remove(uploaded_file.vector_file)

        if os.path.exists(uploaded_file.vector_file):
            os.remove(uploaded_file.vector_file)
        
        uploaded_file.delete()

        messages.success(request, 'Vector database deleted successfully!', extra_tags='safe')

    except UploadedFile.DoesNotExist:
        messages.error(request, 'File not found!', extra_tags='safe')

    return redirect('docs')    


@login_required
def get_or_create_chatroom(request):
	
	other_user = User.objects.get(username = 'pdfai')
	my_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    
	if my_chatrooms.exists():
		for chatroom in my_chatrooms:
			if other_user in chatroom.members.all():
				chatroom = chatroom
				break
			else:
				chatroom = ChatGroup.objects.create(is_private = True)
				chatroom.members.add(other_user, request.user)
	else:
		chatroom = ChatGroup.objects.create(is_private = True)
		chatroom.members.add(other_user, request.user)
        
	return redirect('chatroom', chatroom.group_name)		
 


@login_required
def get_room_to_edit(request):
	my_chatrooms = request.user.chat_groups.filter(is_private=True)
    
	if my_chatrooms.exists():
		for chatroom in my_chatrooms:
			chatroom = chatroom
			break
        
	return redirect('chatroom-edit', chatroom.group_name)



@login_required
def chatroom_delete(request, chatroom_name):
	chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

	if request.method == "POST":
		chat_group.delete()
		messages.success(request, 'chatroom deleted successfully!', extra_tags='safe')
		return redirect('home')


	return render(request, 'chat/delete-chat-room.html', {'chat_group': chat_group})


@login_required
def chatroom_edit(request, chatroom_name):
	chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

	# if request.method == "POST":
	# 	chat_group.delete()
	# 	messages.success(request, 'chatroom deleted successfully!', extra_tags='safe')
	# 	return redirect('home')


	return render(request, 'chat/edit-chat-room.html', {'chat_group': chat_group})

