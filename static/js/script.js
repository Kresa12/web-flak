const  menuIcon = document.getElementById('menu_icon')
const menuList = document.getElementById('menu_list')
// const hiddenh1 = document.getElementsByClassName('hidden_h1')
// const navLink = document.querySelectorAll('.nav_link')
menuIcon.addEventListener('click', () => {
    menuList.classList.toggle('hidden')
    // hiddenh1.classList.toggle('hidden_h1')
})