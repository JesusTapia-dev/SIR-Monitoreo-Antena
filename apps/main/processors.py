def radarsys_globals(request):

    if request.user.is_authenticated:
        theme = request.user.profile.theme
    else:
        theme = 'spacelab'
    return {
        'theme': theme, 
        '{}_active'.format(theme): 'active',
        }