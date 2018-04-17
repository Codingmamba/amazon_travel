from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validate_reg(self, postData):
        print postData
        errors = []
        name = postData['name']
        username = postData['username']
        password = postData['password']
        con_password = postData['con_password']

        # Name
        if len(name) is 0:
            errors.append('Name is required')
        elif len(name) < 3:
            errors.append('Name must be at least 3 characters')

        # Username
        if len(username) is 0:
            errors.append('Username is required')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters')

        # Passwords
        if len(password) is 0:
            errors.append('Password(s) are required')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters')
        elif password != con_password:
            errors.append('Passwords must match')

        if len(errors) > 0:
            return (False, errors)
        else:
            result = self.filter(username=username)
            if len(result) > 0:

                errors.append('Username already exists')
                return (False, errors)
            else:
                new_user = self.create(
                    name = name,
                    username = username,
                    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                )
                return (True, new_user)



    def validate_log(self, postData):
        errors = []
        username = postData['username']
        password = postData['password']

        if len(username) is 0:
            errors.append('Username is required')
        if len(password) is 0:
            errors.append('Password is required')
        if len(errors) > 0:
            
            return (False, errors)
        else:

            results = self.filter(username=username)
            if len(results) > 0:

                user = results[0]
                if bcrypt.checkpw(password.encode(), user.password.encode()):

                    return (True, user)

                else:
                    errors.append('Invalid Username.Password')
                    return (False, errors)
            else:
                errors.append('Invalid Username.Password')
                return (False, errors)



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    travel_from = models.DateField()
    travel_to = models.DateField()
    users = models.ManyToManyField(User, related_name="trips")
    uploader = models.ForeignKey(User, related_name="trip_upload")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.destination
