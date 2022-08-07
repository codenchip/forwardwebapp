from django.shortcuts import render
from django.http import HttpResponse
from forward.settings import MEDIA_URL,MEDIA_ROOT
from django.conf.urls.static import static
from django.views.generic import TemplateView, View 

import numpy as np
import pandas as pd
import matplotlib as pl
pl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sb

class HomePageView(TemplateView):
    def get(self,request,**kwargs):
        return render(request,'combine/index.html',context={'title':'HOME COUNTRY'})

class Api(TemplateView):
    def getNums(request):
        n=np.array([200,366,499])
        name1 = "name-apple" + str(n[1])
        return HttpResponse("{'name':"+name1+",'age':321,'city':'Malaysia'}")

    def getAvg(request):
        s1=request.GET.get("val","")
        if len(s1)==0:
            return HttpResponse("none")
        l1=s1.split(',') #'1,2,3,4,5,6' => ['1','2','3','4','5','6'] => [1,2,3,4,5,6]
        ar=np.array(l1,dtype=int)
        avg=np.average(ar)

        return HttpResponse(str(avg))

    def getGraph(request):
        x = np.arange(0,9 * np.pi, 0.01)
        s = np.cos(x)**2
        plt.plot(x,s)

        plt.xlabel('xlabel(X)')
        plt.ylabel('ylabel(y)')
        plt.title('Basic Graph!')
        plt.grid(True)

        response=HttpResponse(content_type="image/jpeg")
        plt.savefig(response,format="png")
        return response
    
    def getData(request):
        samp = np.random.randint(100,600,size=(4,5))
        df = pd.DataFrame(samp, index=['alex','danny','lina','david'],columns=['Jan','Feb','Mar','Apr','May'])
        return HttpResponse(df.to_html(classes='table table-bordered'))

    def getSeabornGraph(request):
        file_path = MEDIA_ROOT+"/data/titanic_train.csv"
        df = pd.read_csv(file_path)
        graph = sb.factorplot(x='Survived',hue='Sex',data=df, col='Pclass',kind='count')
        response = HttpResponse(content_type="image/jpeg")
        graph.savefig(response, format="png")
        return response

# # Part 2: CHART.JS (Involves Javascript)
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'combine/charts.html')

class ChartData(APIView):
    authentication_classes=[]
    permission_classes=[]

    def get(self,request,format=None):
        labels=['January','February',"March","April","May","June","July"]
        chartLabel="My Data"
        chartData=[0,10,5,2,20,30,45]

        data={
            "labels":labels,
            "chartLabel":chartLabel,
            "chartData":chartData,
        }

        return Response(data)

from plotly.offline import plot
import plotly.graph_objs as go

class PlotlyChartView(TemplateView):
    def get(self, request, *args, **kwargs):
        x_data=[0,1,2,3]
        y_data=[x**2 for x in x_data]
        plot_div = plot([go.Scatter(    
            x=x_data,
            y=y_data,
            mode='lines+markers+text',
            name='My Plotly Chart',
            opacity=0.8,
            marker_color='green'
        )], output_type='div')

        return render(request, 'combine/plotly.html', context={'plot_div':plot_div})

import django_tables2 as tables
from book.models import Book
from hello_world.models import User, UserProfileInfo


# Table Class
class BookTable(tables.Table):
    class Meta:
        model = Book
        attrs = {"class": "table-bordered"}

# View
class BookTableView(tables.SingleTableView):
    table_class=BookTable
    queryset=Book.objects.all()
    template_name="combine/table.html"

# Table Class
class UserTable(tables.Table):
    class Meta:
        model = UserProfileInfo
        attrs = {"class": "table-bordered"}

# View
class UserTableView(tables.SingleTableView):
    table_class=UserTable
    queryset=UserProfileInfo.objects.select_related('user')
    template_name="combine/table.html"