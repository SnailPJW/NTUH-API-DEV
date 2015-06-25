# NTUH API


## Error Codes and Error Messages
---
###1. General cases

- **HTTP401** 101: 帳號密碼錯誤						

- **HTTP401** 102: SessionKey 過期				

- **HTTP403** 103: 無存取權限

- **HTTP404** 104: 請求之資料不存在 (如不存在指定之排程或醫令藥囑)


###2. Patient api relateds

- **HTTP404** 301: 不存在指定之病患

- **HTTP403** 302: 不可瀏覽指定之病患

###3. Bulletin api related

- **HTTP400** 701: 缺少參數 xxx

- **HTTP400** 702: 參數 xxx 型態錯誤。

###4. Order/Medication/Scheduling/Blood related api

- **HTTP400** 801: [排程] 指定之排程順序無法選取 

- **HTTP400** 802: [醫囑] 醫囑相關內容需要修改 細節提示用 message 回傳，不通過的 order request 會回傳對應的 tag 至 failed list 中



## Order Related APIs 
---
### 1. 更新醫療記錄之問題清單答案

- API: */account/{accountNo}/orderRecord/{orderRecordId}/questionary{?limit,offset,sessionKey}*

- method: **PUT**

- parameters: key/value_type should be the **returnKey**/[return_value]:

	** return_value:**
	- for type S, M: the array contains option.returnValue(s)
	- for type D: timestamp (number)
	- for type T, P: string
	
### 2. 開立醫囑或修改醫囑的 Error Response

		+ Response XXX (application/json)
		{
			"error": true,
			"content": {
				"message": "PUT_THE_ERROR_MESSAGE_HERE",
				"failed": [
					"1",			// [string] the tag of the specific failed order
					"2",			// [string] the tag of the specific failed order
					...
				]
			}
		}



