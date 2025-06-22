# 网站分析配置说明

## 百度统计配置

### 1. 获取百度统计ID

1. 访问 [百度统计官网](https://tongji.baidu.com/)
2. 注册/登录百度账号
3. 点击"管理" -> "网站列表" -> "新增网站"
4. 填写网站信息：
   - 网站域名：您的网站域名
   - 网站名称：PIEEG - 低成本脑机接口设备
   - 行业类别：选择相关行业
5. 获取统计代码中的站点ID（形如：`1234567890abcdef`）

### 2. 修改配置文件

在 `hugo.toml` 文件中找到以下配置：

```toml
[params.analytics.baidu]
  enabled = true
  site_id = "your_baidu_site_id_here"  # 请替换为您的百度统计站点ID
```

将 `your_baidu_site_id_here` 替换为您从百度统计获取的实际站点ID。

### 3. 启用/禁用统计

- 启用百度统计：设置 `enabled = true`
- 禁用百度统计：设置 `enabled = false`

### 4. Google Analytics配置（可选）

如果将来需要使用Google Analytics，可以配置：

```toml
[params.analytics.google]
  enabled = true
  tracking_id = "GA_TRACKING_ID"  # 请替换为您的GA跟踪ID
```

### 5. 验证配置

1. 修改配置后重新构建网站：`hugo`
2. 访问网站并在百度统计后台查看是否有数据更新
3. 也可以在浏览器开发者工具中检查是否加载了百度统计脚本

### 6. 注意事项

- 百度统计代码会在每个页面的 `<head>` 部分加载
- 只有当 `enabled = true` 且提供了有效的 `site_id` 时才会加载统计代码
- 统计数据通常需要几小时到24小时才会在百度统计后台显示
- 确保网站域名与百度统计中配置的域名一致

### 7. 配置示例

完整的配置示例：

```toml
[params.analytics]
  # 百度统计
  [params.analytics.baidu]
    enabled = true
    site_id = "1234567890abcdef"
  
  # Google Analytics（可选）
  [params.analytics.google]
    enabled = false
    tracking_id = ""
```

### 8. 隐私说明

建议在网站的隐私政策或免责声明中说明使用了网站分析工具来改善用户体验。 