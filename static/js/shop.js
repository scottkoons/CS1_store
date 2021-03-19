// Delete Product
$('.delete-product').click(deleteProduct);

async function deleteProduct() {
    const id = $(this).data('id');
    await axios.delete(`/api/product/${id}`);
    $(this).closest('tr').remove();
}

// Update Product
$('.update-product').click(updateProduct);

async function updateProduct() {
    const id = $(this).data('id');

    let name = $("#form-name").val();
    let price = $("#form-price").val();
    let stock = $("#form-stock").val();
    let description = $("#form-description").val();
    let image = $("#form-image").val();

    await axios.patch(`/api/product/${id}`, {
        name,
        price,
        stock,
        description,
        image
    });
    window.location.replace("/admin");
}

// $('.delete-order').click(function () {
//     alert("The button was clicked.");
// });

// Delete Order
$('.delete-order').click(deleteOrder);

async function deleteOrder() {
    const id = $(this).data('id');
    await axios.delete(`/admin/order/${id}`);
    $(this).closest('tr').remove();
}

// Controls the tab nav on the view-product.html page
$('#myTab a').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
});