from rest_framework import permissions

class updateownprofile(permissions.BasePermission):
    """giving permissions to user to update their own only profile """

    def has_object_permission(self, request, view, obj):
        """check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id 

class updateownposts(permissions.BasePermission):
    """allow useres to handle their own Posts"""
    def has_object_permission(self, request, view, obj):
        """check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id==request.user.id
