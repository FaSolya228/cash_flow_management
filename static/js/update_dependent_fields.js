const typeSelect = document.querySelector("#id_type");
const categorySelect = document.querySelector("#id_category");
const subcategorySelect = document.querySelector("#id_subcategory");

const BASE_URL = '/api/v1/categories/';

// функция для обновления Select'ов
async function fillSelect(selectElement, url) {
    if (!selectElement) return;

    const valToRestore = selectElement.value || selectElement.getAttribute('data-selected');

    selectElement.disabled = true;

    try {
        const res = await fetch(url);
        const data = await res.json();

        selectElement.innerHTML = '<option value="">---------</option>';
        data.forEach(item => {
            selectElement.add(new Option(item.name, item.id));
        });

        // Восстанавление значения
        if (valToRestore) {
            selectElement.value = valToRestore;

            if (selectElement.value) {
                selectElement.removeAttribute('data-selected');
            }
        }
    } catch (e) {
        console.error(e);
    } finally {
        selectElement.disabled = false;
    }
}

// Изменение поля "Тип"
if (typeSelect) {
    typeSelect.addEventListener("change", async () => {
        const typeId = typeSelect.value;
        const oldCatValue = categorySelect.value;

        await fillSelect(categorySelect, `${BASE_URL}?type=${typeId}&parent__isnull=true`);

        if (oldCatValue) {
            categorySelect.value = oldCatValue;
        }

        if (!categorySelect.value) {
            if (typeId) {
                await fillSelect(subcategorySelect, `${BASE_URL}?type=${typeId}&parent__isnull=false`);
            } else {
                subcategorySelect.innerHTML = '<option value="">---------</option>';
            }
        } else {
            await fillSelect(subcategorySelect, `${BASE_URL}?parent=${categorySelect.value}`);
        }
    });
}

// Изменение поля "Категория"
if (categorySelect) {
    categorySelect.addEventListener("change", async (e) => {
    if (e.detail && e.detail.skipFetch) return;

    const catId = categorySelect.value;
    const typeId = typeSelect.value;

    // Всегда запрашиваем подкатегории
    let params = new URLSearchParams({ parent__isnull: 'false' });

    if (catId) {
        params.append('parent', catId);
    } else if (typeId) {
        params.append('type', typeId);
    }

    // Если catId и typeId пустые, API вернет все подкатегории

    await fillSelect(subcategorySelect, `${BASE_URL}?${params.toString()}`);
});
}

// Изменение поля "Подкатегория"
if (subcategorySelect) {
    subcategorySelect.addEventListener("change", async function() {
    const subId = this.value;

    if (!subId) {
        // Если подкатегорию сбросили, то возвращаем полные списки категорий и типов
        await fillSelect(categorySelect, `${BASE_URL}?parent__isnull=true`);
        return;
    }

    const res = await fetch(`${BASE_URL}${subId}/`);
    const data = await res.json();

    if (data.type && typeSelect) {
        typeSelect.value = data.type;
        // обрезаем список категорий по типу
        await fillSelect(categorySelect, `${BASE_URL}?type=${data.type}&parent__isnull=true`);
    }

    if (data.parent && categorySelect) {
        categorySelect.value = data.parent;
    }
});
}

window.addEventListener('load', () => {
    if (categorySelect && categorySelect.value) {
        // Запускаем цепочку обновлений для уже выбранных значений
        categorySelect.dispatchEvent(new Event('change'));
    }
});