---
layout: post
title: a post with jupyter notebook
date: 2023-07-04 08:57:00-0400
description: an example of a blog post with jupyter notebook
categories: sample-posts jupyter-notebook
giscus_comments: true
related_posts: false
---

To include a jupyter notebook in a post, you can use the following code:

{% raw %}

```html
{::nomarkdown}
{% assign jupyter_path = "assets/jupyter/blog.ipynb" | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/blog.ipynb %}{% endcapture %}
{% if notebook_exists == "true" %}
    {% jupyter_notebook jupyter_path %}
{% else %}
    <p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}
```

{% endraw %}

Let's break it down: this is possible thanks to [Jekyll Jupyter Notebook plugin](https://github.com/red-data-tools/jekyll-jupyter-notebook) that allows you to embed jupyter notebooks in your posts. It basically calls [`jupyter nbconvert --to html`](https://nbconvert.readthedocs.io/en/latest/usage.html#convert-html) to convert the notebook to an html page and then includes it in the post. Since [Kramdown](https://jekyllrb.com/docs/configuration/markdown/) is the default Markdown renderer for Jekyll, we need to surround the call to the plugin with the [::nomarkdown](https://kramdown.gettalong.org/syntax.html#extensions) tag so that it stops processing this part with Kramdown and outputs the content as-is.

The plugin takes as input the path to the notebook, but it assumes the file exists. If you want to check if the file exists before calling the plugin, you can use the `file_exists` filter. This avoids getting a 404 error from the plugin and ending up displaying the main page inside of it instead. If the file does not exist, you can output a message to the user. The code displayed above outputs the following:

{::nomarkdown}
{% assign jupyter_path = "assets/jupyter/blog.ipynb" | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/blog.ipynb %}{% endcapture %}
{% if notebook_exists == "true" %}
    {% jupyter_notebook jupyter_path %}
{% else %}
    <p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}

Note that the jupyter notebook supports both light and dark themes.

# Jupyter Notebooks on AWS

After creating EC2 instance follow the following steps to run a jupyter notebook. Jupyter notebook uses port 8888 to access the web interface. When you create the instance make sure to add port 8888 under security policy configurations before launching so that you will be able access your jupyter notebook later.

### 1. Install Conda (Miniconda)

From the official website [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html) find the right link based on your python version.

![python-versions](assets/img/python_versions.png)

Copy the address link and download the setup file using

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh
```

Run the setup

```python
chmod +x ./Miniconda3-py38_4.11.0-Linux-x86_64.sh && ./Miniconda3-py38_4.11.0-Linux-x86_64.sh
```

### Install Jupyter Lab

Using conda install Jupyter lab using

```bash
conda install -c conda-forge jupyterlab
```

**Setup password**

Inside ~/.jupyter directory create a new file ` jupyter_server_config.py`

```bash
touch .jupyter/jupyter_server_config.py
```

```bash
c.ServerApp.ip = '*' # bind to any network interface
c.ServerApp.password = u'<your hashed password here>'
c.ServerApp.open_browser = False
c.ServerApp.port = 8888 # or any other ports you'd like
```

To setup a jupyter password

```bash
jupyter server password
```

The above command will ask you to enter a password. Once you’re done, you will get a json file with jupyter_server_config name. Copy the hashed password from this file and past it to ` jupyter_server_config.py`.

You’re done! run jupyter lab and use your public ip to access your notebook.

## Attach EFS

— attach EFS to the instance

1. Create efs
You can go to AWS's EFS and create an efs. This will allow you to store your important data even after you closed your EC2 instance

2. Mount the efs
After creating efs, you will find a button that says "Attach". Click on it and you'll find a command to execture on your terminal to attach the efs. But before that make sure to create `efs` folder in your instance.
    
```bash
sudo mount ******.amazonaws.com:/ efs
```
    
3. 
This is an optional command. It allows you to used the temporary storage instance available along with your EC2.

```bash
sudo mkfs -t xfs /dev/nvme1n1
```

4. Mount the storage

```bash
sudo mkdir ~/data && sudo mount /dev/nvme1n1 ~/data
```

5. 

```bash
sudo chmod go+rw data
```

6. Extract your data

```bash
tar -xf efs/*.tar && source .bashrc
```

### All Combined

```bash
mkdir efs
sudo mount *** .amazonaws.com:/ efs
sudo mkfs -t xfs /dev/nvme1n1
sudo mkdir ~/data && sudo mount /dev/nvme1n1 ~/data
sudo chmod go+rw ~/data
tar -xf efs/*.tar && source .bashrc
```

### Persist config data to EFS

If you want to store your data fter you're done with your work;

```bash
sudo tar -cf ~/efs/*.tar ./miniconda3 .kaggle .ipython .jupyter .conda .bashrc
```

## Python 3.8

1. sudo apt install python3.8
2. sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
3. sudo update-alternatives --config python

Note: this note is adapted from https://chen-zhe.github.io/blog/p/aws-user-notes-for-deep-learning/
