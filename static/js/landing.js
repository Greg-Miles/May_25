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
});