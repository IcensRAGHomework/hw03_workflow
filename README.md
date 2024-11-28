# Chromadb 作業題目

## 作業內容

請使用 **chromadb** 套件完成以下作業，並實作提供的方法 `generate_hw01-04(question)`。實作於 **`student_assignment.py`** 中。

---

### 作業1

1. **問題**：`2024年台灣10月紀念日有哪些?`(範例)
2. **方法**：實作 `generate_hw01(question)`，用於回答上述問題。
3. **輸出格式**：
   - JSON 格式如下：
     ```json
     {
         "Result": 
             {
                 "date": "2024-10-10",
                 "name": "國慶日"
             }
     }
     ```

---

### 作業2

1. **問題**：`2024年台灣10月紀念日有哪些?`(範例)
2. **方法**：
   - 使用 Function Calling 的方式查詢指定的 API。
   - 實作 `generate_hw02(question)`，用於回答上述問題。
3. **指定 API**：
   - 使用 [Calendarific API](https://calendarific.com/)。
   - 步驟：
     1. 訪問 Calendarific 網站並註冊帳戶。
     2. 登錄後進入 Dashboard，取得您的 API Key。
4. **輸出格式**：
   - JSON 格式如下：
     ```json
     {
         "Result": 
             {
                 "date": "2024-10-10",
                 "name": "國慶日"
             }
     }
     ```

---

### 作業3

1. **問題**：`根據先前的節日清單，這個節日是否有在該月份清單？{"date": "10-31", "name": "蔣公誕辰紀念日"}'`(範例)
2. **方法**：
   - 使用 ConversationBufferMemory 的方式記憶前一次的回答。
   - 實作 `generate_hw03(question1, question2)`，用於回答上述問題。 PS.question1是作業2的問題
3. **輸出格式**：
   - JSON 格式如下：
     ```json
     {
         "Result": 
             {
                 "add": true,
                 "reason": "蔣中正誕辰紀念日並未包含在十月的節日清單中。目前十月的現有節日包括國慶日、重陽節、華僑節、台灣光復節和萬聖節。因此，如果該日被認定為節日，應該將其新增至清單中。"
             }
     }
     ```

---

### 作業4

1. **問題**：`請問中華台北的積分是多少`(範例)
2. **方法**：
   - 使用提供的圖片檔案 baseball.png 作為輸入數據來源，透過程式實現圖片內容的解析與問題的回答。
   - 實作 `generate_hw04(question)`，用於回答上述問題。
3. **輸出格式**：
   - JSON 格式如下：
     ```json
     {
         "Result": 
             {
                 "score": 5478
             }
     }
     ```

---

### 注意事項
- 必須使用 **LangChain** 套件完成方法實作。
- 確保輸出的格式與範例一致。

### 參考來源
- [參考1](https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html)
- [參考2](https://learn.microsoft.com/zh-tw/azure/ai-services/openai/how-to/gpt-with-vision?tabs=rest)
- [參考3](https://python.langchain.com/v0.1/docs/modules/memory/types/buffer/)
- [參考4](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/openai_functions_agent/)

