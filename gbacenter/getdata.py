from lxml import etree

with open('project.mch',mode='r',encoding='utf-8') as f:
    content = f.read()

# 解析 XML 数据
root = etree.fromstring(content)

# 使用 XPath 查询命令节点
commands = root.xpath("//CommandDocBase")

# with open("commands.csv", mode='w', encoding='utf-8') as f:
# # 遍历每个命令节点并提取属性数据
#     for command in commands:
#         Id = command.get("Id")
#         Name = command.get("Name")
#         NetworkType = command.get("NetworkType")
#         NetworkIP = command.get("NetworkIP")
#         NetworkPort = command.get("NetworkPort")
#         CommandData = command.get("CommandData")
#         f.write(f"{Id},{Name},{NetworkType},{NetworkIP},{NetworkPort},{CommandData}\n")
#
#         print(f"Id: {Id}")
#         print(f"Name: {Name}")
#         print(f"NetworkType: {NetworkType}")
#         print(f"NetworkIP: {NetworkIP}")
#         print(f"NetworkPort: {NetworkPort}")
#         print(f"CommandData: {CommandData}")
#         print("-------------")

# 使用 XPath 查询命令组节点
command_groups = root.xpath("//CommandGroupDocBase")

# 遍历每个命令组节点并提取属性数据和子元素数据
for command_group in command_groups:
    Type = command_group.get("type")
    Id = command_group.get("Id")
    Name = command_group.get("Name")

    # 查询子元素 <CommandIds> 下的 <unsignedInt> 元素
    command_ids = command_group.xpath(".//unsignedInt/text()")

    print(f"type: {Type}")
    print(f"Id: {Id}")
    print(f"Name: {Name}")
    print("CommandIds:", command_ids)
    print("-------------")

# 解析 XML 数据
root = etree.fromstring(content)

# 使用 XPath 查询命令组节点
command_groups = root.xpath("//CommandGroupDocBase")

with open('command_group.csv', mode='w', encoding='utf-8') as f:
    # 遍历每个命令组节点
    for command_group in command_groups:
        ls = []
        element_type = command_group.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        Id = command_group.get("Id")
        Name = command_group.get("Name")
        ls.append(element_type)
        ls.append(Id)
        ls.append(Name)
        print(f"Type: {element_type}")
        print(f"Id: {Id}")
        print(f"Name: {Name}")
        if "Sequence" in element_type:

            # 查询子元素 <CommandSequence> 下的所有 <CommandSequenceItemDoc> 元素
            sequence_items = command_group.xpath(".//CommandSequenceItemDoc")

            # 遍历每个序列项并提取属性数据
            for sequence_item in sequence_items:
                Delay = sequence_item.get("Delay")
                CommandId = sequence_item.get("CommandId")
                print(f"  Delay: {Delay}")
                print(f"  CommandId: {CommandId}")
                ls.append(Delay)
                ls.append(CommandId)

        else:
            # 查询子元素 <CommandIds> 下的 <unsignedInt> 元素
            command_ids = command_group.xpath(".//unsignedInt/text()")
            ls+=command_ids



        str_ls = ','.join(ls) + '\n'

        f.write(str_ls)

        print("-------------")