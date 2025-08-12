package com.crud.web3app.service;

import com.crud.web3app.model.DataItem;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.gas.DefaultGasProvider;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

@Service
public class Web3Service {
    private final Web3j web3j;
    private final DataStorage contract;
    private final Credentials credentials;

    public Web3Service(
            @Value("${web3j.network}") String networkUrl,
            @Value("${web3j.contract.address}") String contractAddress,
            @Value("${web3j.wallet.private-key}") String privateKey) {
        this.web3j = Web3j.build(new HttpService(networkUrl));
        this.credentials = Credentials.create(privateKey);
        this.contract = DataStorage.load(
                contractAddress,
                web3j,
                credentials,
                new DefaultGasProvider());
    }

    public DataItem createData(String name, String description) throws Exception {
        var txReceipt = contract.create(name, description).send();
        var events = txReceipt.getLogs();
        /// ////////////
        int id = contract.nextId().send().intValue() - 1;

        return new DataItem(id, name, description);
    }

    public DataItem getData(int id) throws Exception {
        var result = contract.read(BigInteger.valueOf(id)).send();

        return new DataItem(
                result.component1().intValue(),
                result.component2(),
                result.component3());
    }

    public List<DataItem> getAllData() throws Exception {
        List<DataItem> items = new ArrayList<>();
        var count  = contract.nextId().send().intValue() - 1;
        for (int i = 1; i <= count; i++) {
            var result = contract.read(BigInteger.valueOf(i)).send();
            if (result.component1().intValue != 0) {
                items.add(new DataItem(
                        result.component1().intValue(),
                        result.component2(),
                        result.component3()));
            }
        }

        return items;
    }

    public DataItem updateData(int id, String name, String description) throws Exception {
        contract.update(BigInteger.valueOf(id), name, description).send();

        return new DataItem(id, name, description);
    }

    public void deleteData(int id) throws Exception {
        contract.remove(BigInteger.valueOf(id)).send();
    }
}
