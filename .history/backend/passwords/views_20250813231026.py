from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PasswordEntry
from .serializers import PasswordEntrySerializer
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

# Generate a key for encryption (in production, store this securely)
def get_encryption_key():
    """Get or create encryption key"""
    key_file = os.path.join(settings.BASE_DIR, 'encryption_key.key')
    
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
    
    return key

def encrypt_password(password):
    """Encrypt password"""
    key = get_encryption_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return base64.b64encode(encrypted_password).decode()

def decrypt_password(encrypted_password):
    """Decrypt password"""
    key = get_encryption_key()
    fernet = Fernet(key)
    decoded_password = base64.b64decode(encrypted_password.encode())
    decrypted_password = fernet.decrypt(decoded_password)
    return decrypted_password.decode()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def password_list(request):
    """List user's passwords or create new password"""
    
    if request.method == 'GET':
        # Get all passwords for the current user
        passwords = PasswordEntry.objects.filter(user=request.user)
        
        # Decrypt passwords before sending
        password_data = []
        for password_entry in passwords:
            data = PasswordEntrySerializer(password_entry).data
            try:
                data['decrypted_password'] = decrypt_password(password_entry.encrypted_password)
            except:
                data['decrypted_password'] = 'Error decrypting'
            password_data.append(data)
        
        return Response(password_data)
    
    elif request.method == 'POST':
        # Create new password entry
        try:
            site_name = request.data.get('site_name')
            site_url = request.data.get('site_url', '')
            username = request.data.get('username')
            password = request.data.get('password')
            notes = request.data.get('notes', '')
            
            if not site_name or not username or not password:
                return Response({
                    'error': 'Site name, username, and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Encrypt password
            encrypted_password = encrypt_password(password)
            
            # Create password entry
            password_entry = PasswordEntry.objects.create(
                user=request.user,
                site_name=site_name,
                site_url=site_url,
                username=username,
                encrypted_password=encrypted_password,
                notes=notes
            )
            
            return Response({
                'message': 'Password saved successfully',
                'password': PasswordEntrySerializer(password_entry).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': 'Failed to save password'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def password_detail(request, pk):
    """Get, update, or delete a specific password"""
    
    try:
        password_entry = PasswordEntry.objects.get(pk=pk, user=request.user)
    except PasswordEntry.DoesNotExist:
        return Response({
            'error': 'Password not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = PasswordEntrySerializer(password_entry).data
        try:
            data['decrypted_password'] = decrypt_password(password_entry.encrypted_password)
        except:
            data['decrypted_password'] = 'Error decrypting'
        return Response(data)
    
    elif request.method == 'PUT':
        # Update password entry
        try:
            site_name = request.data.get('site_name', password_entry.site_name)
            site_url = request.data.get('site_url', password_entry.site_url)
            username = request.data.get('username', password_entry.username)
            password = request.data.get('password')
            notes = request.data.get('notes', password_entry.notes)
            
            password_entry.site_name = site_name
            password_entry.site_url = site_url
            password_entry.username = username
            password_entry.notes = notes
            
            # Only encrypt new password if provided
            if password:
                password_entry.encrypted_password = encrypt_password(password)
            
            password_entry.save()
            
            return Response({
                'message': 'Password updated successfully',
                'password': PasswordEntrySerializer(password_entry).data
            })
            
        except Exception as e:
            return Response({
                'error': 'Failed to update password'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        password_entry.delete()
        return Response({
            'message': 'Password deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)