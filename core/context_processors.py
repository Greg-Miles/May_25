from django.urls import resolve

def page_titles(request):
    """
    Добавляет название страницы в контекст всех шаблонов
    """
    url_name = resolve(request.path_info).url_name
    
    # Словарь с названиями страниц
    titles = {
        'landing': 'Барбершоп "Горшок"',
        'orders_list': 'Список заявок',
        'masters': 'Наши мастера',
        'services_list': 'Услуги',
        'contacts': 'Контакты',
        # Добавьте другие URL-имена и соответствующие заголовки
    }
    
    # Получаем название для текущего URL или используем дефолтное значение
    page_title = titles.get(url_name, titles['landing'])
    
    return {'page_title': page_title}