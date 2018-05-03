#ifndef CMD_HADNLERS_LXD_H
#define CMD_HADNLERS_LXD_H

#include <cmd_handlers.h>

/*********************************************
 * Any actions with the container. Actions: create, start, stop and delete container
**********************************************/

class CmdHandlerLXDContainers : public CmdHandlerBase {

    public:
        CmdHandlerLXDContainers();
        virtual void handle(ModelRequest *pRequest);

    private:
        std::string TAG;

        void create_container(std::string name, QJsonObject &jsonResponse);
        void start_container(std::string name, QJsonObject &jsonResponse);
        void stop_container(std::string name, QJsonObject &jsonResponse);
        void delete_container(std::string name, QJsonObject &jsonResponse);
};

REGISTRY_CMD(CmdHandlerLXDContainers)

/*********************************************
 * Get information about the orhestra, containers.
**********************************************/

class CmdHandlerLXDInfo : public CmdHandlerBase {

    public:
        CmdHandlerLXDInfo();
        virtual void handle(ModelRequest *pRequest);
};

REGISTRY_CMD(CmdHandlerLXDInfo)

/*********************************************
 * Get information about all containers.
**********************************************/

class CmdHandlerLXDList : public CmdHandlerBase {

    public:
        CmdHandlerLXDList();
        virtual void handle(ModelRequest *pRequest);
};

REGISTRY_CMD(CmdHandlerLXDList)

#endif // CMD_HADNLERS_LXD_H