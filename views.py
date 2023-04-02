import datetime
from rest_framework import viewsets, filters
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from api.service import is_client_secret_token
from django_filters.rest_framework import DjangoFilterBackend


@api_view(['GET'])
def Company_list(request):
    try:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        final_end_date = end_datetime + datetime.timedelta(days=1)
        list = Company.objects.filter(added_date__gte=start_date).filter(
            added_date__lte=final_end_date)
        serializer_Company_info = CompanySerializer(
            list, many=True, context={'request': request})
        return Response(serializer_Company_info.data)
    except Exception as e:
            print(e)
            return Response({'error': str(e)})


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['name', 'location', 'type']
    search_fields = ['name', 'location', 'type']
    ordering_fields = ['company_id']

    @method_decorator(is_client_secret_token)
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        try:
            company = Company.objects.get(pk=pk)
            emps = Employee.objects.filter(company=company)
            emps_serializer = EmployeeSerializer(
                emps, many=True, context={'request': request})
            return Response(emps_serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message': 'Company might not exit !! Error'
            })


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['name', 'email', 'phone']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['id', 'name', 'company']
