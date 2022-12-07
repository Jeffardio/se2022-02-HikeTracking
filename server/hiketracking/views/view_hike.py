import geopy.distance
from django.http import FileResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from hiketracking.models import Hike, Point, HikeReferencePoint, CustomUser
from hiketracking.utility import get_province_and_village


class HikeFile( APIView ):
    # permission_classes = (permissions.AllowAny,)

    def get(self, request, hike_id):
        try:
            track = Hike.objects.get( id=hike_id ).track_file
            return FileResponse( open( str( track ), 'rb' ) )
        except Exception as e:
            print( e )
            return Response( status=status.HTTP_500_INTERNAL_SERVER_ERROR )

    def put(self, request, hike_id):
        try:
            file = request.FILES['File']
        except Exception as e:
            Hike.objects.filter( id=hike_id ).delete()
            return Response( status=status.HTTP_400_BAD_REQUEST, data={"Error": "File Requested"} )

        try:
            hike = Hike.objects.get( id=hike_id )
            hike.track_file = file
            hike.save()
            return Response( status=status.HTTP_200_OK )
        except Exception as e:
            Hike.objects.filter( id=hike_id ).delete()
            return Response( status=status.HTTP_400_BAD_REQUEST, data={"Error": "Hike not found"} )


class Hikes( APIView ):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):

        filters = request.GET.get( 'filters', None )

        if filters:
            minLength = request.GET.get( 'minLength', None )
            maxLength = request.GET.get( 'maxLength', None )
            minTime = request.GET.get( 'minTime', None )
            maxTime = request.GET.get( 'maxTime', None )
            minAscent = request.GET.get( 'minAscent', None )
            maxAscent = request.GET.get( 'maxAscent', None )
            difficulty = request.GET.get( 'difficulty', None )
            province = request.GET.get( 'province', None )
            village = request.GET.get( 'village', None )

            hikes = Hike.objects.all()

            if minLength:
                hikes = hikes.filter( length__gte=minLength )
            if maxLength:
                hikes = hikes.filter( length__lte=maxLength )
            if minTime:
                hikes = hikes.filter( expected_time__gte=minTime )
            if maxTime:
                hikes = hikes.filter( expected_time__lte=maxTime )
            if minAscent:
                hikes = hikes.filter( ascent__gt=minAscent )
            if maxAscent:
                hikes = hikes.filter( ascent__lte=maxAscent )
            if difficulty:
                hikes = hikes.filter( difficulty=difficulty )

            if province:
                inner_query = Point.objects.filter( province=province )
                hikes = hikes.filter( start_point__in=inner_query )

            if village:
                inner_query = Point.objects.filter( village=village.lower().capitalize() )
                hikes = hikes.filter( start_point__in=inner_query )

            hikes = hikes.values()

        else:
            hikes = Hike.objects.values()

        around = request.GET.get( 'around', None )

        if filters and around:
            filtered_hikes = []
            fields = around.split( "-" )
            radius = fields[2]
            input_coordinates = (fields[0], fields[1])

            for h in hikes:
                refer_p = Point.objects.get( id=h['start_point_id'] )
                hike_coordinates = (refer_p.latitude, refer_p.longitude)
                distance = geopy.distance.geodesic(
                    input_coordinates, hike_coordinates ).km

                if distance <= float( radius ):
                    filtered_hikes.append( h )

            hikes = filtered_hikes

        result = {}
        for h in hikes:
            result = HikeReferencePoint.objects.filter(
                hike_id=h['id'] ).values()
            list = []
            for r in result:
                refer_p = Point.objects.get( id=r['point_id'] )
                list.append( {
                    'reference_point_lat': refer_p.latitude,
                    'reference_point_lng': refer_p.longitude,
                    'reference_point_address': refer_p.address} )

            h['rp'] = list

            startP = Point.objects.get( id=h['start_point_id'] )
            endP = Point.objects.get( id=h['end_point_id'] )

            h['start_point_lat'] = startP.latitude
            h['start_point_lng'] = startP.longitude
            h['start_point_address'] = startP.address
            h['end_point_lat'] = endP.latitude
            h['end_point_lng'] = endP.longitude
            h['end_point_address'] = endP.address

        return Response( hikes, status=status.HTTP_200_OK )

    def post(self, request):
        user_id = CustomUser.objects.get( email=request.user )
        data = request.data

        try:
            sp = get_province_and_village(
                data['start_point_lat'], data['start_point_lng'] )
            start_point_type = 'none'

            start_point = Point.objects.get_or_create(
                latitude=data['start_point_lat'],
                longitude=data['start_point_lng'],
                defaults={
                    'province': sp['province'],
                    'village': sp['village'],
                    'address': data['start_point_address'],
                    'type': start_point_type
                }
            )

            ep = get_province_and_village(
                data['end_point_lat'], data['end_point_lng'] )
            end_point_type = 'none'

            end_point = Point.objects.get_or_create(
                latitude=data['end_point_lat'],
                longitude=data['end_point_lng'],
                defaults={
                    'province': ep['province'],
                    'village': ep['village'],
                    'address': data['end_point_address'],
                    'type': end_point_type
                }
            )

            hike = Hike.objects.create(
                title=data['title'],
                length=data['length'],
                expected_time=data['expected_time'],
                ascent=data['ascent'],
                difficulty=data['difficulty'],
                description=data['description'],
                local_guide=user_id,
                start_point=start_point[0],
                end_point=end_point[0] )

            hike.save()

            for rp in data['rp_list']:
                rp_cp = get_province_and_village(
                    rp['reference_point_lat'], rp['reference_point_lng'] )
                ref_point_type = 'none'
                ref_point = Point.objects.get_or_create(
                    latitude=rp['reference_point_lat'],
                    longitude=rp['reference_point_lng'],
                    defaults={
                        'province': rp_cp['province'],
                        'village': rp_cp['village'],
                        'address': rp['reference_point_address'],
                        'type': ref_point_type
                    }
                )

                rp_hike = HikeReferencePoint.objects.create(
                    hike=hike,
                    point=ref_point[0]
                )
                rp_hike.save()

            return Response( status=status.HTTP_200_OK, data={"hike_id": hike.id} )
        except Exception as e:
            print( e )
            return Response( status=status.HTTP_400_BAD_REQUEST, data={"Error": str( e )} )
