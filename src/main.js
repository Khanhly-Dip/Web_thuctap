$(document).ready(function () {
    const $wrapper = $('#logo-wrapper'); // Chọn danh sách logo
    const $items = $('#logo-wrapper a');
    const visibleItems = 1; // Số lượng phần tử hiển thị
    const itemWidth = $items.outerWidth(true);
    // const itemWidth = 60; // Chiều rộng mỗi logo (điều chỉnh phù hợp)
    const scrollAmount = visibleItems * itemWidth; // Tổng khoảng cách cần cuộn
    let currentIndex = 0; // Vị trí hiện tại


    // Sự kiện cho nút trái
    $('#prev').click(function () {
        console.log("nnnnnn")
        if (currentIndex > 0) {
            currentIndex--;
            $wrapper.css('transform', `translateX(-${currentIndex * itemWidth}px)`);
        } else {
            currentIndex = Math.ceil($wrapper.children().length / visibleItems) - 1;
        }
        $wrapper.css('transform', `translateX(-${currentIndex * scrollAmount}px)`);
    });

    // Sự kiện cho nút phải
    $('#next').click(function () {
        // clearInterval(autoSlide); // Dừng slideshow tự động khi nhấn nút
        if (currentIndex < Math.ceil($wrapper.children().length / visibleItems) - 1) {
            currentIndex++;
            $wrapper.css('transform', `translateX(-${currentIndex * itemWidth}px)`);
        } else {
            currentIndex = 0;
        }
        $wrapper.css('transform', `translateX(-${currentIndex * scrollAmount}px)`);
    });
});