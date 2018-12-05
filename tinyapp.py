from django.conf.urls import url
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.decorators.http import require_http_methods

DEBUG = True
SECRET_KEY = 'This is a secret'
ROOT_URLCONF = __name__
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        './static'
    ],
}]

@require_http_methods(['GET'])
def index(req):

    template = get_template('index.html')
    html = template.render()

    return HttpResponse(html)

@require_http_methods(['POST'])
def upload(req):

    file = req.FILES['file']

    # do processing here

    template = get_template('upload.html')
    html = template.render({ 'filename': file.name })

    return HttpResponse(html)

urlpatterns = [
    url('^$', index),
    url('^upload/?$', upload)
]

print('i am debugging :)')
