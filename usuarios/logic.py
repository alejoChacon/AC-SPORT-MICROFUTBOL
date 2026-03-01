def encriptar_contraseña(user):
    if user:
        print(user)
        user.set_password('gemelo4348M')
        user.save()
        return {'message':f'Contraseña se encripto correctamente!'}
    return print('Hubo un error')