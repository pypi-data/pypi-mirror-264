<h1 align="center">pysvn_util</h1>

- svn_util.py

操作svn的各种封装方法，使用示例：

```python
# 使用示例
svn_client = SVNClient(repo_url='svn://', working_copy_path='', username='',
                       password='')
checkout_output, checkout_error, checkout_code = svn_client.checkout()
logging.info(f'检出日志: {checkout_output}')
logging.error(f'检出错误: {checkout_error}')
logging.info(f'检出返回码: {checkout_code}')

update_output, update_error, update_code = svn_client.update()
logging.info(f'更新日志: {update_output}')
logging.error(f'更新错误: {update_error}')
logging.info(f'更新返回码: {update_code}')

add_output, add_error, add_code = svn_client.add("/app/temp/svn/nginx/2")
logging.info(f'增加日志: {add_output}')
logging.error(f'增加错误: {add_error}')
logging.info(f'增加返回码: {add_code}')

commit_output, commit_error, commit_code = svn_client.commit('Committing changes')
logging.info(f'提交日志: {commit_output}')
logging.error(f'提交错误: {commit_error}')
logging.info(f'提交返回码: {commit_code}')
```
