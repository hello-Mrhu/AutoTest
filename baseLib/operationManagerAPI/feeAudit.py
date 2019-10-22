import requests
from baseLib.commonAPI import OracleQuery
from configuration import const
from baseLib.baseUtils.recorder import runningRecorder

#费率审核
@runningRecorder(desc='费率审核通过')
def merchantFeeAuditAction_auditConfirm(merchantFeeRequestId, cookie):
    merchantFeeAuditActionList = ['/Admin/merchantManage/merchantFeeAuditAction_auditConfirm']
    merchantFeeAuditResponse = requests.get(const._global_configuration().OptionManagerHttpUrl + merchantFeeAuditActionList[0] + '?requestId=' + merchantFeeRequestId,
                                            cookies = cookie)
    responseHtmlStr = merchantFeeAuditResponse.text
    strSQL = 'select status from MERCHANT_FEE_REQUEST where id = %s order by id desc' % merchantFeeRequestId
    return OracleQuery.sqlAll(strSQL)

#费率审核
@runningRecorder(desc='费率审核拒绝')
def merchantFeeAuditAction_auditCancel(merchantFeeRequestId, cookie):
    merchantFeeAuditActionList = ['/Admin/merchantManage/merchantFeeAuditAction_auditCancel']
    merchantFeeAuditResponse = requests.get(const._global_configuration().OptionManagerHttpUrl + merchantFeeAuditActionList[0] + '?requestId=' + merchantFeeRequestId + '&reason=test',
                                            cookies = cookie)
    responseHtmlStr = merchantFeeAuditResponse.text
    strSQL = 'select status from MERCHANT_FEE_REQUEST where id = %s order by id desc' % merchantFeeRequestId
    return OracleQuery.sqlAll(strSQL)