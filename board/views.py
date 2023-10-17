from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

from .models import Board, Comment
from django.urls import reverse
from django.shortcuts import redirect
from .forms import BoardForm
from .forms import CommentForm


def index(request):
    board_list = Board.get_active_list().prefetch_related('comment_set').all()

    return render(request, "board/index.html",
                  {'board_list': board_list})


def board_detail(request, board_id):
    board = Board.objects.get(pk=board_id)
    if not (board and board.is_active):
        return Http404("요청하신 페이지가 없습니다.")

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comment(
                content=data['content'],
                board_id=board_id
            ).save()
            return redirect(reverse('board:detail',
                                    kwargs={'board_id': board_id}))

    return render(request,
                  "board/detail.html",
                  {'board': board, 'form': form})



def board_write(request):
    form = BoardForm()
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('borad:index'))
        pass
    return render(request, 
                  'board/write.html',
                  {'form': form})

def board_edit(request, board_id):
    board = Board.objects.get(id=board_id)
    form = BoardForm(initial={
        'title': board.title,
        'content': board.content,
        'author': board.author
    })
    if request.method == 'POST':
        form = BoardForm(request.POST)

        if form.is_valid():
            board.title = form.cleaned_data['title']
            board.content = form.cleaned_data['content']
            board.author = form.cleaned_data['author']
            board.save()
            return redirect(reverse('board:detail', kwargs={
                'board_id': board_id
            }))
    return render(request,
                  "board/edit.html",
                  {'form': form})


def board_delete(request, board_id):
    board = Board.objects.get(id=board_id)
    board.is_delete = True
    board.save()
    return redirect(reverse('board:index'))



# def index(request):
#     return HttpResponse("Hello World, I am Younsoo!")


"""
board_list라는 view 함수를 만들고 /board 로 접속하면 
게시글에 대한 전체 게시글을 리스트 (HTML: ul, li 태그 이용)로 보여주세요. 
"""


# def board_list(request):
#     qs = Board.objects.all()

#     html = ""
#     for board in qs:
#         html += "<li>{board.title}</li>"
#     html = f"<ul>{html}</ul>"

#     return HttpResponse(html)



# def comment_list(request):
#     qs = Comment.objects.all()
#     html = ""
#     for comment in qs:
#         commnet += f'<li>{comment.id} | \
#             {comment.content} | {comment.board_id} </li>'
#         html = f'<ul>{html}</ul>'

#     return HttpResponse(html)


# def board_detail(request, board_id):
#     qs = Board.objects.get(id=board_id)
#     comment_list = qs.comment_set.all()

#     html = f'<h1>{qs.title}</h1> \
#         <div> {qs.content}</div>'
    
#     html += '<ul>'
#     for comment in comment_list:
#         html += f'<li>{comment_list}</li>'
#         html += '</ul>'

#     return HttpResponse(html)

