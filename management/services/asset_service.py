# management/services/asset_service.py
from bson import ObjectId
from mongoengine.queryset import Q
from mongoengine.errors import DoesNotExist
from datetime import datetime
import math
from management.models.asset import Asset
from management.models.document_embedded import DocumentEmbedded

class AssetService:
  
  @staticmethod
  def get_assets_list(page_number=1, per_page=10, search_query='', code_query=''):
    """Obtener lista paginada de activos con filtros"""
    try:
      page_number = int(page_number)
      per_page = int(per_page)
    except (ValueError, TypeError):
      page_number = 1
      per_page = 10
    
    if page_number < 1:
      page_number = 1
    if per_page < 1:
      per_page = 10

    assets = Asset.objects.all()
    
    query_list = []
    if search_query:
      query_list.append(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    if code_query:
      query_list.append(Q(code__icontains=code_query))

    if query_list:
      combined_query = query_list[0]
      for q in query_list[1:]:
        combined_query &= q
      assets = assets.filter(combined_query)

    total_assets = assets.count()
    total_pages = math.ceil(total_assets / per_page)
    
    offset = (page_number - 1) * per_page
    paginated_assets = assets.skip(offset).limit(per_page)

    return {
      'assets': paginated_assets,
      'total_assets': total_assets,
      'total_pages': total_pages,
      'page_number': page_number,
      'per_page': per_page,
      'offset': offset
    }
  
  @staticmethod
  def get_asset_by_id(asset_id):
    """Obtener activo por ID"""
    try:
      return Asset.objects.get(id=ObjectId(asset_id))
    except Asset.DoesNotExist:
      return None
    except Exception:
      return None
  
  @staticmethod
  def create_asset(name, description, code):
    """Crear nuevo activo"""
    try:
      asset = Asset(
        name=name,
        description=description,
        code=code,
        documents=[]
      )
      asset.save()
      return asset, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def update_asset(asset_id, name, description, code):
    """Actualizar activo existente"""
    try:
      asset = AssetService.get_asset_by_id(asset_id)
      if not asset:
        return None, "Activo no encontrado"
      
      asset.name = name
      asset.description = description
      asset.code = code
      asset.save()
      
      return asset, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def delete_asset(asset_id):
    """Eliminar activo"""
    try:
      asset = AssetService.get_asset_by_id(asset_id)
      if not asset:
        return False, "Activo no encontrado"
      
      asset_name = asset.name
      asset.delete()
      return True, asset_name
    except Exception as e:
      return False, str(e)
  
  @staticmethod
  def add_document_to_asset(asset_id, name, size, mime, url):
    """Agregar documento a un activo"""
    try:
      asset = AssetService.get_asset_by_id(asset_id)
      if not asset:
        return None, "Activo no encontrado"
      
      document = DocumentEmbedded(
        name=name,
        size=size,
        mime=mime,
        url=url
      )
      
      asset.documents.append(document)
      asset.save()
      return asset, None
    except Exception as e:
      return None, str(e)
  
  @staticmethod
  def delete_document_from_asset(asset_id, document_id):
    """Eliminar documento de un activo"""
    try:
      asset = AssetService.get_asset_by_id(asset_id)
      if not asset:
        return False, "Activo no encontrado"
      
      document_to_delete = None
      for doc in asset.documents:
        if str(doc.id) == document_id:
          document_to_delete = doc
          break
      
      if not document_to_delete:
        return False, "Documento no encontrado"
      
      asset.documents.remove(document_to_delete)
      asset.save()
      return True, None
    except Exception as e:
      return False, str(e)