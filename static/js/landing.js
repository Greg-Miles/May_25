document.addEventListener('DOMContentLoaded', function() {
    const appointment = document.querySelector('.make_appointment_btn');
    if (appointment) {
        appointment.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            window.location.href = url||'/new_order/';
        });
    } else {
        console.error('Кнопки нет.');
    }
    const appointmentWithMaster = document.querySelector('.make_appointment_with_master');
    if (appointmentWithMaster) {
        appointmentWithMaster.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            window.location.href = url;
        });
    }
    
    // Код для автоматического закрытия сообщений
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            // Проверяем, доступен ли bootstrap.Alert
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                // Если bootstrap.Alert недоступен, используем простое скрытие
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.style.display = 'none';
                }, 500); // Задержка для анимации исчезновения
            }
        });
    }, 5000); // Закрыть через 5 секунд

    // Код для карточек мастеров
    const masterCards = document.querySelectorAll('.master-card');
    if (masterCards.length > 0) {
        masterCards.forEach(function(card) {
            // Добавляем класс для стилизации при наведении
            card.classList.add('master-card-hover');
            
            // Получаем ID мастера из атрибута data-master-id
            const masterId = card.getAttribute('data-master-id');
            
            // Добавляем обработчик клика
            card.addEventListener('click', function() {
                if (masterId) {
                    window.location.href = `/master/${masterId}/`;
                }
            });
            
            // Добавляем стиль курсора, чтобы показать, что элемент кликабельный
            card.style.cursor = 'pointer';
        });
    }

    // Код для динамического обновления списка услуг при выборе мастера
    const masterSelect = document.getElementById('id_master');
    const servicesSelect = document.getElementById('id_services');
    
    if (masterSelect && servicesSelect) {
        masterSelect.addEventListener('change', function() {
            const masterId = this.value;
            
            // Очищаем список услуг
            servicesSelect.innerHTML = '';
            
            if (masterId) {
                // Делаем AJAX запрос для получения услуг мастера
                fetch(`/get_master_services/?master_id=${masterId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.services && data.services.length > 0) {
                            data.services.forEach(service => {
                                const option = document.createElement('option');
                                option.value = service.id;
                                option.textContent = `${service.name} - ${service.price} руб.`;
                                servicesSelect.appendChild(option);
                            });
                        } else {
                            const option = document.createElement('option');
                            option.value = '';
                            option.textContent = 'У этого мастера нет доступных услуг';
                            option.disabled = true;
                            servicesSelect.appendChild(option);
                        }
                    })
                    .catch(error => {
                        console.error('Ошибка при загрузке услуг:', error);
                        const option = document.createElement('option');
                        option.value = '';
                        option.textContent = 'Ошибка загрузки услуг';
                        option.disabled = true;
                        servicesSelect.appendChild(option);
                    });
            } else {
                // Если мастер не выбран, показываем сообщение
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'Сначала выберите мастера';
                option.disabled = true;
                servicesSelect.appendChild(option);
            }
        });
        
        // Инициализируем список услуг при загрузке страницы
        if (masterSelect.value) {
            masterSelect.dispatchEvent(new Event('change'));
        } else {
            // Если мастер не выбран, показываем сообщение
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Сначала выберите мастера';
            option.disabled = true;
            servicesSelect.appendChild(option);
        }
    }

});