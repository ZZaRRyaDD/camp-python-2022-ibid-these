let url = new URL(location);
let orderSelect = document.querySelector("select#order");
let categorySelect = document.querySelector("select#category");
let statusSelect = document.querySelector("select#status");
const ORDERING_PARAM = "order";
const PAGE_PARAM = "page";
const CATEGORY_PARAM = "category";
const STATUS_PARAM = "status";

if (url.searchParams.get(ORDERING_PARAM)) {
  let itemOrder = document.querySelector(
    `option[value=${url.searchParams.get(ORDERING_PARAM)}]`
  );
  itemOrder.selected = true;
}

if (url.searchParams.get(CATEGORY_PARAM)) {
  let itemCategory = document.querySelector(
    `option[value=${url.searchParams.get(CATEGORY_PARAM)}]`
  );
  itemCategory.selected = true;
}

if (url.searchParams.get(STATUS_PARAM)) {
  let itemStatus = document.querySelector(
    `option[value=${url.searchParams.get(STATUS_PARAM)}]`
  );
  itemStatus.selected = true;
}

if (orderSelect) {
  orderSelect.addEventListener("change", function (event) {
    let selectedValue = orderSelect.children[event.target.selectedIndex].value;
    if (selectedValue) {
      url.searchParams.set(ORDERING_PARAM, selectedValue);
      url.searchParams.set(PAGE_PARAM, 1);
    } else {
      url.searchParams.delete(ORDERING_PARAM);
      url.searchParams.delete(PAGE_PARAM);
    }
    location = url.href;
  });
}

if (categorySelect) {
  categorySelect.addEventListener("change", function (event) {
    let selectedValue = categorySelect.children[event.target.selectedIndex].value;
    let urlList = document.querySelector("nav.navbar").dataset.lotsListUrl;
    url.pathname = (url.pathname !== urlList) ? urlList: url.pathname
    if (selectedValue) {
      url.searchParams.set(CATEGORY_PARAM, selectedValue);
      url.searchParams.set(PAGE_PARAM, 1);
    } else {
      url.searchParams.delete(CATEGORY_PARAM);
      url.searchParams.delete(PAGE_PARAM);
    }
    location = url.href;
  });
}

if (statusSelect) {
  statusSelect.addEventListener("change", function (event) {
    let selectedValue = statusSelect.children[event.target.selectedIndex].value;
    if (selectedValue) {
      url.searchParams.set(STATUS_PARAM, selectedValue);
      url.searchParams.set(PAGE_PARAM, 1);
    } else {
      url.searchParams.delete(STATUS_PARAM);
      url.searchParams.delete(PAGE_PARAM);
    }
    location = url.href;
  });
}

let prevArrow = document.querySelector("li.page-item button.prev-arrow");
let nextArrow = document.querySelector("li.page-item button.next-arrow");
let prevPage = document.querySelector("li.page-item button.page-link.prev-page");
let nextPage = document.querySelector("li.page-item button.page-link.next-page");

if (prevArrow) {
  prevArrow.addEventListener("click", function (event) {
    redirectToPage(prevArrow);
  });
}

if (nextArrow) {
  nextArrow.addEventListener("click", function (event) {
    redirectToPage(nextArrow);
  });
}

if (prevPage) {
  prevPage.addEventListener("click", function (event) {
    redirectToPage(prevPage);
  });
}

if (nextPage) {
  nextPage.addEventListener("click", function (event) {
    redirectToPage(nextPage);
  });
}

function redirectToPage(item) {
  url.searchParams.set(PAGE_PARAM, Number(item.dataset.page));
  location = url.href;
}
