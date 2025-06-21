// PIEEG 管理后台 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // 侧边栏折叠/展开
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('active');
        });
    }
    
    // 侧边栏下拉菜单
    const dropdownItems = document.querySelectorAll('.sidebar-dropdown > a');
    
    dropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const parent = this.parentElement;
            parent.classList.toggle('active');
        });
    });
    
    // 自动展开当前活动的下拉菜单
    const activeDropdown = document.querySelector('.sidebar-dropdown.active');
    if (activeDropdown) {
        const submenu = activeDropdown.querySelector('.sidebar-submenu');
        if (submenu) {
            submenu.style.display = 'block';
        }
    }
    
    // 文件上传标签更新
    const customFileInputs = document.querySelectorAll('.custom-file-input');
    customFileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const fileName = this.files[0]?.name || '选择文件';
            const label = this.nextElementSibling;
            if (label) {
                label.textContent = fileName;
            }
        });
    });
    
    // 表单提交前显示加载动画
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // 检查是否有必填字段未填
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                }
            });
            
            if (isValid) {
                // 创建并显示加载动画
                const spinner = document.createElement('div');
                spinner.className = 'spinner-overlay';
                spinner.innerHTML = '<div class="spinner-border" role="status"><span class="sr-only">加载中...</span></div>';
                document.body.appendChild(spinner);
            }
        });
    });
    
    // 确认删除操作
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm || '确定要执行此操作吗？')) {
                e.preventDefault();
            }
        });
    });
    
    // 表格排序
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const sortKey = this.dataset.sort;
            const currentOrder = this.dataset.order || 'asc';
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            
            // 更新URL参数
            const url = new URL(window.location);
            url.searchParams.set('sort', sortKey);
            url.searchParams.set('order', newOrder);
            window.location = url;
        });
    });
    
    // 批量操作
    const bulkActionForm = document.getElementById('bulk-action-form');
    const bulkActionSelect = document.getElementById('bulk-action');
    const bulkCheckboxes = document.querySelectorAll('.bulk-checkbox');
    
    if (bulkActionForm && bulkActionSelect) {
        bulkActionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const selectedIds = Array.from(bulkCheckboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);
            
            if (selectedIds.length === 0) {
                alert('请至少选择一项');
                return;
            }
            
            const action = bulkActionSelect.value;
            if (!action) {
                alert('请选择要执行的操作');
                return;
            }
            
            if (confirm('确定要对所选项执行此操作吗？')) {
                // 创建隐藏字段存储选中的ID
                selectedIds.forEach(id => {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'ids[]';
                    input.value = id;
                    bulkActionForm.appendChild(input);
                });
                
                bulkActionForm.submit();
            }
        });
    }
    
    // 全选/取消全选
    const selectAllCheckbox = document.getElementById('select-all');
    if (selectAllCheckbox && bulkCheckboxes.length > 0) {
        selectAllCheckbox.addEventListener('change', function() {
            bulkCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
        
        // 当单个复选框状态变化时，更新全选框状态
        bulkCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const allChecked = Array.from(bulkCheckboxes).every(cb => cb.checked);
                const someChecked = Array.from(bulkCheckboxes).some(cb => cb.checked);
                
                selectAllCheckbox.checked = allChecked;
                selectAllCheckbox.indeterminate = someChecked && !allChecked;
            });
        });
    }
});
