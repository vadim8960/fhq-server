#include "update_user_location_task.h"
#include <QThread>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QEventLoop>
#include <fallen.h>
#include <employ_database.h>
#include <QSqlQuery> // TODO redesign
#include <QSqlRecord> // TODO redesign
#include <wsjcpp_geoip.h>

UpdateUserLocationTask::UpdateUserLocationTask(int userid, const std::string &sLastIP) {
    m_nUserID = userid;
    m_sLastIP = sLastIP;
    TAG = "UpdateUserLocationTask";
}

UpdateUserLocationTask::~UpdateUserLocationTask() {
    
}

void UpdateUserLocationTask::run() {
    if (m_sLastIP == "::1") {
        WSJCppLog::info(TAG, "Skip " + m_sLastIP);
        return;
    }
    WSJCppLog::info(TAG, "userid = " + std::to_string(m_nUserID) + " start");
    EmployDatabase *pDatabase = findWSJCppEmploy<EmployDatabase>();

    QSqlDatabase db = *(pDatabase->database());
    QSqlQuery query(db);
    query.prepare("SELECT * FROM users WHERE id = :id");
    query.bindValue(":id", m_nUserID);
    if (!query.exec()) {
        WSJCppLog::err(TAG, query.lastError().text().toStdString());
    }
    if (query.next()) {
        QSqlRecord record = query.record();
        std::string sLastIP = record.value("last_ip").toString().toStdString();

        if (sLastIP != m_sLastIP) {
            // TODO redesign to curl request
            // TODO redesign check in database same ip first
            WSJCppLog::info(TAG, "Update user # " + std::to_string(m_nUserID) + " location by ip " + m_sLastIP);
            QNetworkAccessManager manager;

            WSJCppGeoIPResult res = WSJCppGeoIP::requestToIpApiCom(m_sLastIP);
            if (res.hasError()) {
                WSJCppLog::info(TAG, m_sLastIP + " -> " + res.getErrorDescription());
            } else {
                WSJCppLog::info(TAG, "userid = " + std::to_string(m_nUserID) + ", update last_ip, city, region, country");

                QSqlQuery query_update(db);
                query_update.prepare("UPDATE users SET "
                    "last_ip = :lastip,"
                    "country = :country,"
                    "region = :region,"
                    "city = :city,"
                    "latitude = :latitude,"
                    "longitude = :longitude "
                    " WHERE id = :id");
                query_update.bindValue(":lastip", QString::fromStdString(m_sLastIP));
                query_update.bindValue(":country", QString::fromStdString(res.getCountry()));
                query_update.bindValue(":region", QString::fromStdString(res.getRegionName()));
                query_update.bindValue(":city", QString::fromStdString(res.getCity()));
                query_update.bindValue(":latitude", res.getLatitude());
                query_update.bindValue(":longitude", res.getLongitude());
                query_update.bindValue(":id", m_nUserID);
                if (!query_update.exec()) {
                    WSJCppLog::err(TAG, query_update.lastError().text().toStdString());
                }
            }
        } else {
            WSJCppLog::info(TAG, "IP address same for userid = " + std::to_string(m_nUserID));    
        }
    } else {
        WSJCppLog::err(TAG, "failed for userid = " + std::to_string(m_nUserID) + "(not found userid in database)");
    }
};
