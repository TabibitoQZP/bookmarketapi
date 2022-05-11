from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import json

from .models import Book, Profile, Cargo, Bill
from django.contrib.auth.models import User

# Create your views here.

def userInfo(request):
    if(request.method=='GET'):
        print(request.GET)
        if(request.GET['gettype']=='0'):
            tmpUser=User.objects.get(username=request.GET['username'])
            print('filter',len(Profile.objects.filter(user=tmpUser)))
            if(len(Profile.objects.filter(user=tmpUser))==0):
                # 创建一个简易的空对象
                tmp=Profile()
                # 该给的都给一下, 省的报错
                tmp.realname='null'
                tmp.man=True
                tmp.user=tmpUser
                tmp.birth='2000-1-1'
                tmp.save()
            p=Profile.objects.get(user=tmpUser)
            rtdict ={}
            rtdict['realname']=p.realname
            rtdict['id']=p.id
            rtdict['man']=p.man
            rtdict['birth']=p.birth
            print(rtdict)
            return JsonResponse(rtdict)
        elif(request.GET['gettype']=='1'):
            tmpUser=User.objects.get(username=request.GET['username'])
            p=Profile.objects.get(user=tmpUser)
            p.realname=request.GET['realname']
            p.man=True if request.GET['man']=='true' else False
            p.birth=request.GET['birth']
            p.save()
            return JsonResponse({'message': '啥b'})
    return JsonResponse({'message': '啥b'})

def LogIn(request):
    if(request.method=='GET'):
        print(request.GET)
        tmpUser=User.objects.get(username=request.GET['username'])
        if(tmpUser.check_password(request.GET['password'])):
            return JsonResponse({'res':True})
        else:
            return JsonResponse({'res':False})
    return JsonResponse({'res':False})

def Books(request):
    if(request.method=='GET'):
        print(request.GET)
        # 0nothing, 1change, 2sale, 3search
        if(request.GET['gettype']=='0'):
            tmp = Book.objects.all()
            ret = [model_to_dict(i) for i in tmp]
            return JsonResponse({'res':ret})
        elif(request.GET['gettype']=='5'):
            tmp=Book()
            newBook=json.loads(request.GET['newBook'])
            tmp.ISBN=newBook['ISBN']
            tmp.name=newBook['name']
            tmp.author=newBook['author']
            tmp.public=newBook['public']
            tmp.remain=int(newBook['remain'])
            tmp.price=float(newBook['price'])
            tmp.save()
            return JsonResponse({})
        elif(request.GET['gettype']=='4'):
            bookinfo=json.loads(request.GET['row'])
            newCargo=Cargo()
            newCargo.price=float(request.GET['price'])
            newCargo.amount=int(request.GET['amount'])
            newCargo.status='i'
            newCargo.book=Book.objects.get(ISBN=bookinfo['ISBN'])
            newCargo.save()
            # 注意还没付款呢...
            # newBill=Bill()
            # newBill.earn=-newCargo.price*newCargo.amount
            # tmpbook=Book.objects.get(ISBN=bookinfo['ISBN'])
            # tmpbook.remain+=int(request.GET['amount'])
            # tmpbook.save()
            # newBill.save()
            return JsonResponse({})
        elif(request.GET['gettype']=='2'):
            newBill=Bill()
            bookinfo=json.loads(request.GET['row'])
            newBill.earn=float(bookinfo['price'])*int(request.GET['saleNum'])
            newBill.save()
            tmpbook=Book.objects.get(ISBN=bookinfo['ISBN'])
            tmpbook.remain-=int(request.GET['saleNum'])
            tmpbook.save()
            return JsonResponse({})
        elif(request.GET['gettype']=='3'):
            cSearch = json.loads(request.GET['search'])
            print(cSearch)
            books=Book.objects.all()
            if(cSearch['type']=='1'):
                tmp=books.filter(ISBN__contains=cSearch['info'])
            elif(cSearch['type']=='2'):
                tmp=books.filter(name__contains=cSearch['info'])
            elif(cSearch['type']=='3'):
                tmp=books.filter(author__contains=cSearch['info'])
            elif(cSearch['type']=='4'):
                tmp=books.filter(public__contains=cSearch['info'])
            else:
                tmp=books.filter(ISBN__contains=cSearch['info'])|\
                    books.filter(name__contains=cSearch['info'])|\
                    books.filter(author__contains=cSearch['info'])|\
                    books.filter(public__contains=cSearch['info'])
            ret = [model_to_dict(i) for i in tmp]
            return JsonResponse({'res':ret})
        elif(request.GET['gettype']=='1'):
            cBook = json.loads(request.GET['row'])
            print(cBook['ISBN'])
            tmp = Book.objects.get(ISBN=cBook['ISBN'])
            tmp.name=cBook['name']
            tmp.author=cBook['author']
            tmp.public=cBook['public']
            tmp.remain=cBook['remain']
            tmp.price=cBook['price']
            tmp.save()
            print(tmp)
            return JsonResponse({'res':''})
    return HttpResponse('books')

def Cargos(request):
    if(request.method=='GET'):
        if(request.GET['gettype']=='0'):
            tmp = Cargo.objects.filter(status='i')
            ret = [model_to_dict(i) for i in tmp]
            for i in ret:
                tmpname = Book.objects.get(ISBN=i['book']).name
                i['bookname']=tmpname
            # ret =[i['book']=Book.objects.get(ISBN=i['book']).name for i in ret]
            # print(ret)
            return JsonResponse({'res':ret})
        # 修改状态i未付款, j已付款记得扣钱书籍增加, k退货无事发生
        elif(request.GET['gettype']=='1'):
            tmploads=json.loads(request.GET['row'])
            newCargo=Cargo.objects.get(id=tmploads['id'])
            if(tmploads['status']=='已付款'):
                newBill=Bill()
                newBill.earn=-newCargo.price*newCargo.amount
                tmpbook=Book.objects.get(ISBN=tmploads['book'])
                tmpbook.remain+=int(tmploads['amount'])
                tmpbook.save()
                newBill.save()
                newCargo.status='j'
                newCargo.save()
            elif(tmploads['status']=='已退货'):
                newCargo.status='k'
                newCargo.save()
            return JsonResponse({})
    return JsonResponse({})

def Bills(request):
    if(request.method=='GET'):
        tmp=Bill.objects.all()
        ret = [model_to_dict(i) for i in tmp]
        return JsonResponse({'res':ret})
    return JsonResponse({})
        