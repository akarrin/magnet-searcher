# -*- coding:utf-8 -*-
import re

def highlight_keyword(keyword, sentence):
    '''
    高亮字符串中的关键词,以字典形式返回
    :param keyword: 需要高亮的关键词
    :param sentence: 需要处理的字符串
    :return: 区分高亮部分和未高亮部分字符串的字典
    '''
    chinese_pattern = re.compile(u'[\u4e00-\u9fa5]')
    chinese_keyword_list =  re.findall(chinese_pattern, keyword) # 中文以每个单字作为关键字
    non_chinese_keyword = re.sub(chinese_pattern,'', keyword.lower())
    non_chinese_keyword_list = re.findall('\w+', non_chinese_keyword)  # 其他字符串以单词作为关键词
    keyword_list = chinese_keyword_list + non_chinese_keyword_list
    highlight_pattern = '|'.join(keyword_list)  # 拼接关键词正则模式'keyword1|keyword2|keyword3'
    sentence_split_list = []
    start_position = 0
    keyword_positions = re.finditer(highlight_pattern, sentence.lower())  # 关键词在sentence中的位置
    if keyword_positions:
        for a_keyword_position in keyword_positions:
            position_span = a_keyword_position.span()
            no_highlight_part = sentence[start_position: position_span[0]]
            if no_highlight_part:
                sentence_split_list.append({'is_highlight': 0, 'text': no_highlight_part})
            highlight_part = sentence[position_span[0]: position_span[1]]
            if highlight_part:
                sentence_split_list.append({'is_highlight': 1, 'text': highlight_part})
            start_position = position_span[1]
        no_highlight_part = sentence[start_position:]
        if no_highlight_part:
            sentence_split_list.append({'is_highlight': 0, 'text': no_highlight_part})
    else:
        sentence_split_list.append({'is_highlight': 0, 'text': sentence})
    return sentence_split_list