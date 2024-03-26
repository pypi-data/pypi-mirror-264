# OS-Copilot: Towards Generalist Computer Agents with Self-Improvement

<div align="center">

[[Website]](https://os-copilot.github.io/)
[[Arxiv]](https://arxiv.org/abs/2402.07456)
[[PDF]](https://arxiv.org/pdf/2402.07456.pdf)
[[Documentation]]()
<!-- [[Tweet]](https://twitter.com/DrJimFan/status/1662115266933972993?s=20) -->

[![Static Badge](https://img.shields.io/badge/MIT-License-green)](https://github.com/OS-Copilot/OS-Copilot/blob/main/LICENSE)
![Static Badge](https://img.shields.io/badge/python-3.10-blue)
[![Static Badge](https://img.shields.io/badge/FRIDAY-Frontend-yellow)](https://github.com/OS-Copilot/FRIDAY-front)



<p align="center">
  <img src='pic/demo.png' width="100%">
</p>

</div>

## 📖 Overview

- **OS-Copilot** is a pioneering conceptual framework for building generalist computer agents on Linux and MacOS, which provides a unified interface for app interactions in the heterogeneous OS ecosystem.
  
<p align="center">
  <img src='pic/framework.png' width="75%">
</p>

- Leveraging OS-Copilot, we built **FRIDAY**, a self-improving AI assistant capable of solving general computer tasks.

<p align="center">
  <img src='pic/FRIDAY.png' width="75%">
</p>

## ⚡️ Quickstart

1. **Clone the GitHub Repository:** 

   ```
   git clone https://github.com/OS-Copilot/OS-Copilot.git
   ```

2. **Set Up Python Environment:** Ensure you have a version 3.10 or higher Python environment. You can create and
   activate this environment using the following commands, replacing `oscopilot_env` with your preferred environment
   name:

   ```
   conda create -n oscopilot_env python=3.10 -y
   conda activate oscopilot_env
   ```

3. **Install Dependencies:** Move into the `OS-Copilot` directory and install the necessary dependencies by running:

   ```
   cd OS-Copilot
   pip install -e .
   ```

4. **Set OpenAI API Key:** Configure your OpenAI API key in [.env](.env) and select the model you wish to use.

5. **Running the Script:** Run the quick_start.py script, simply execute the following command in your terminal:
   ```
   python quick_start.py
   ```

\* FRIDAY currently only supports single-round conversation.

## 🛠️ FRIDAY-Gizmos
We maintain an open-source library of toolkits for FRIDAY, which includes tools that can be directly utilized within FRIDAY.
For a detailed list of tools, please see [FRIDAY-Gizmos](https://github.com/OS-Copilot/FRIDAY-Gizmos). The usage methods are as follows:

1. Find the tool you want to use in [FRIDAY-Gizmos](https://github.com/OS-Copilot/FRIDAY-Gizmos) and download its tool code.
2. Add the tool to FRIDAY's toolkit:
```shell
python friday/tool_repository/manager/tool_manager.py --add --tool_name [tool_name] --tool_path [tool_path]
```
3. If you wish to remove a tool, you can run:
```shell
python friday/tool_repository/manager/tool_manager.py --delete --tool_name [tool_name]
```

## 💻 User Interface (UI)

**Enhance Your Experience with Our Intuitive Frontend!** This interface is crafted for effortless control of your agents. For more details, visit [FRIDAY Frontend](https://github.com/OS-Copilot/FRIDAY-front).

## ✨ Deploy API Services

For comprehensive guidelines on deploying API services, please refer to the [OS-Copilot documentation](). 


<!-- ## 👨‍💻‍ Contributors

<a href="">
  <img src="" />
</a>

Made with [contrib.rocks](https://contrib.rocks). -->

## 🛡 Disclaimer

OS-Copilot is provided "as is" without warranty of any kind. Users assume full responsibility for any risks associated with its use, including **potential data loss** or **changes to system settings**. The developers of OS-Copilot are not liable for any damages or losses resulting from its use. Users must ensure their actions comply with applicable laws and regulations.


## 🏫 Community

Join our community to connect with other agent enthusiasts, share your tools and demos, and collaborate on exciting initiatives. You can find us on [Slack](https://join.slack.com/t/slack-ped8294/shared_invite/zt-2cqebow90-soac9UFKGZ2RcUy8PqjZrA).


## 🔎 Citation

```
@misc{wu2024oscopilot,
      title={OS-Copilot: Towards Generalist Computer Agents with Self-Improvement}, 
      author={Zhiyong Wu and Chengcheng Han and Zichen Ding and Zhenmin Weng and Zhoumianze Liu and Shunyu Yao and Tao Yu and Lingpeng Kong},
      year={2024},
      eprint={2402.07456},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```


## 📬 Contact

If you have any inquiries, suggestions, or wish to contact us for any reason, we warmly invite you to email us at wuzhiyong@pjlab.org.cn.