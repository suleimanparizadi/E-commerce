from apps.menu.models import menu_model
from utils.service_result import ServiceResult
from django.db import transaction
from apps.menu.tasks import generate_qr_code


class MenuService:

    def __init__(self, user):
        self.user = user


    @transaction.atomic
    def create_menu(self, title, description=None):

    
        menu = menu_model.QRMenu.objects.create(
            user=self.user,
            title=title,
            description=description
        )

        menu_section = menu_model.MenuSection.objects.create(
            menu=menu,
            name="Main",
            order=0
        )


        if menu:

            # means its only works when the database transaction successfully commits.  
            transaction.on_commit(
                
                # just to give is as attribute not to execute  
                lambda:generate_qr_code.delay(menu.id)
            )


            return ServiceResult.success(
                data={'menu':menu,
                        'qr_code':menu.qr_code,
                        'menu_section':menu_section},
                message="menu created successfully."
                )

        return ServiceResult.fail(
            message="unable to create menu"
        )




    def delete_menu(self, menu_id):

        try:
            menu = menu_model.QRMenu.objects.get(id=menu_id, user=self.user)

        except menu_model.QRMenu.DoesNotExist:
            return ServiceResult.fail(
                message="unable to locate the menu."
            )
        
        if menu.qr_code and menu.qr_code.storage.exists(menu.qr_code.name):
            menu.qr_code.delete(save=False)

        menu.delete()        



        return ServiceResult.success(
            message="menu deleted successfully."
        )
        

