# 果壳 Cache 验证报告

> 位于根目录.PDF

## 验证环境与代码

> 位于 cache-ut/testbench

## 运行及复现方式

> make clean && make init && clear && make test && make report

---

```tree
cache-ut/
├── Cache                           - picker 生成的 Cache 模块
│   └── ...
├── NutShell                        - 果壳 NutShell 子模块
│   └── ...
├── build                           - Chisel 生成的 RTL 代码
│   └── Cache.v
├── out                             - Mill 的默认输出目录
│   └── ...
├── reports                         - toffee 生成的 html 报告
│   └── ...
├── src                             - Mill 生成 Cache 的 Chisel 代码
│   └── main
├── testbench                       + 整个 toffee-test 验证框架，项目主要代码位于此
│   ├── bundle
│   ├── coverage
│   ├── env
│   └── ...
├── tests                           + 所有测试用例，项目剩余的代码位于此
│   └── test_*.py
├── wavout                          - 测试记录的波形
│   └── Cache.fst
├── pyproject.toml
└── build.sc
```
